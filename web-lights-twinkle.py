# Pico Lights Plus - AP Mode
# Code for controlling LED lights using the
# Pico Lights board 
# Also needs secrets.py with WiFi login details
from machine import Pin, PWM
from utime import sleep
import network
import socket
import uasyncio as asyncio
import secrets
import re
import random
from url_handler import URL_Handler


# Mode can be ap (access point where the Pico acts as a web server)
# or "client" [default] which connects to an existing network
# Note that client mode is blocking and will not run the rest of the code
# until a network connection is established
mode="client"

# All documents in DocumentRoot are publically accessible
DocumentRoot = "public/"

# Simplify code by using FULL_IN instead of 65535 (max 16bit value) used for duty cycle
FULL_ON = 65535

# Indexed at 0 (board labelling is 1)
# These must be the same length (ie 3)
outputs = (20, 19, 18)
switches = (3, 4, 5)

# shortened version for the pin objects
out = []
sw = []
# start with twinkle on channel 1
action = ["twinkle", "static", "static"]
# Count of the intervals between flashes
count = [0,0,0]

twinkle_seq = [32000,32000,50000,65535,65535,65535,50000,32000,32000,32000,32000,32000]

# Flash rate = number of times each loop before changing
flash_rate = 10

url = URL_Handler(DocumentRoot)

# Count how long between button presses
button_count = 0
# How long between button presses
button_delay = 10

# Functions control both output and led
def turn_on (pin):
    out[pin].duty_u16(FULL_ON)
    action[pin] = "static"
    
def turn_off (pin):
    out[pin].duty_u16(0)
    action[pin] = "static"

# Uses out to toggle - sets led to same
def toggle_out (pin):
    # If off turn on
    if action[pin] == "static" and out[pin].duty_u16()<32000:
        out[pin].duty_u16(FULL_ON)
        action[pin] = "static"
    # if on change to flash
    elif action[pin] == "static" and out[pin].duty_u16()>=32000:
        action[pin] = "flash"
    elif action[pin] == "flash":
        action[pin] = "twinkle"
    else:
        action[pin] = "static"
        out[pin].duty_u16(0)

# Performs flash - based on 50:50 
def flash (pin):
    if count[pin] < flash_rate:
        out[pin].duty_u16(FULL_ON)
        #print ("On")
    else:
        out[pin].duty_u16(0)
        #print ("Off")
    count[pin] += 1
    if count[pin] > (2 * flash_rate):
        count[pin] = 0


def twinkle (pin):
    count_num = count[pin]
    if count_num < len(twinkle_seq):
        out[pin].duty_u16(twinkle_seq[count_num])
        count[pin] += 1
    # if passed end of seq then one in 6 chance of resetting (only if 0)
    else:
#        rand_no = random.randint(0,4)
#        if rand_no == 0:
#            count[pin] = 0
        count[pin] = 0
        

# Twinkle - short flashes
def twinkle_old (pin):
    if count[pin] < 4:
        out[pin].duty_u16(FULL_ON)
    else:
        out[pin].duty_u16(FULL_ON)
        #print ("Off")
    count[pin] += 1
    if count[pin] > 9:
        count[pin] = 0

def connect():
    #Connect to WLAN
    if mode== "ap":
        # Access Point mode
        ip = connect_ap_mode()
    else:
        ip = connect_client_mode()
    return ip
    


def connect_ap_mode ():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=secrets.SSID, password=secrets.PASSWORD)
    wlan.active(True)
    while wlan.active() == False:
        print ('Trying to setup AP mode')
    ip = wlan.ifconfig()[0]
    print('AP Mode is active')
    print('Connect to Wireless Network '+secrets.SSID)
    print('Connect to IP address '+ip)
    return ip

def connect_client_mode ():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power saving mode
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print('Connect to IP address '+ip)    
    return ip



def setup_pins ():
    # uses length of outputs
    for i in range (0, len(outputs)):
        out.append(PWM(Pin(outputs[i]), freq=300_000))
        sw.append(Pin(switches[i], Pin.IN, Pin.PULL_UP))


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = request_line.decode("utf-8")
    
    # LED change request (returns own string)
    led_change = url.change_led(request)
    if led_change != None:
        if (led_change[1] == "toggle"):
            toggle_out (led_change[0])
        elif (led_change[1] == "on"):
            turn_on (led_change[0])
        elif (led_change[1] == "off"):
            turn_off (led_change[0])
        elif (led_change[1] == "flash"):
            action[led_change[0]] = "flash"
        elif (led_change[1] == "twinkle"):
            action[led_change[0]] = "twinkle"
        # Ignore any other values (code doesn't support any)
        # Return status - currently just text (will change to JSON)
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/text\r\n\r\n')
        writer.write('Status ...')
    
    
    else:
        # Otherwise is this is static file request
        
        url_value, url_file, url_type = url.validate_file(request)

        writer.write('HTTP/1.0 {} OK\r\nContent-type: {}\r\n\r\n'.format(url_value, url_type))
        # Send file 1kB at a time (avoid problem with large files exceeding available memory)
        with open(DocumentRoot+url_file, "rb") as read_file:
            data = read_file.read(1024)
            while data:
                writer.write(data)
                await writer.drain()
                data = read_file.read(1024)
            read_file.close()

    await writer.wait_closed()
    print("Client disconnected")


# Initialise Wifi
async def main ():
    # Set Status LED to Red (power on)
    setup_pins ()
    print ("Connecting to network")
    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset
    print ("IP address", ip)
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print ("Web server listening on", ip)
    while True:
        #onboard.on()
        # Enable following line for heartbeat debug messages
        #print ("heartbeat")
        await asyncio.sleep(0.08)
        # Check gpio pins 10 times between checks for webpage (5 secs)
        check_gpio_buttons()
        # If flash or toggle then call appropriate function
        for i in range (0, 3):
            if action[i] == "twinkle":
                twinkle (i)
            elif action[i] == "flash":
                flash (i)
        
# Main loop
def check_gpio_buttons ():
    global button_count, button_delay
    # Only check if button_count = 0
    if button_count < button_delay:
        button_count += 1
        return
    else:
        button_count = 0
        
    for i in range (0, len(sw)):
        if sw[i].value() == 0:
            toggle_out(i)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()