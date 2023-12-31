from machine import Pin
from utime import sleep
import network
import socket
import uasyncio as asyncio
import secrets
import re

# Indexed at 0 (board labelling is 1)
# These must be the same length (ie 3)
outputs = (20, 19, 18)
switches = (3, 4, 5)

# shortened version for the pin objects
out = []
sw = []

html = """<!DOCTYPE html>
<html>
<head> <title>Pico Lights Plus</title> </head>
<body> <h1>Pico Lights Plus</h1>
<ul>
<li><a href="/lights?light=1&action=toggle">LED 1</a></li>
<li><a href="/lights?light=2&action=toggle">LED 2</a></li>
<li><a href="/lights?light=3&action=toggle">LED 3</a></li>
</ul>
</body>
</html>
"""

# Uses out to toggle - sets led to same
def toggle_out (pin):
    new_state = 1 - out[pin].value()
    print ("Setting out {} to {}".format(pin, new_state))
    out[pin].value(new_state)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power saving mode
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def setup_pins ():
    # uses length of outputs
    for i in range (0, len(outputs)):
        out.append(Pin(outputs[i], Pin.OUT))
        sw.append(Pin(switches[i], Pin.IN, Pin.PULL_UP))

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    # Regular expressing Looking for toggle request
    m = re.search ('light=(\d)&action=toggle', request_line)
    if m != None:
        led_selected = int(m.group(1))-1
        # check valid number
        if (led_selected >=0 and led_selected <= 2) :
            print ("LED selected "+str(led_selected))
            toggle_out (led_selected)

    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(html)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")


# Initialise Wifi
async def main ():
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
        await asyncio.sleep(0.25)
        # Check gpio pins 10 times between checks for webpage (5 secs)
        for i in range (0, 5):
            check_gpio_buttons()
    
# Main loop
def check_gpio_buttons ():
    for i in range (0, len(sw)):
        if sw[i].value() == 0:
            toggle_out(i)
    sleep (0.5)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()