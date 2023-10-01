# pico-lights
Raspberry Pi Pico LED Light Controller

Controls LED low-voltage lighting using a Raspberry Pi Pico and the Pico Lights Board.

# Code

There are two different programs included. The basic program is simple-lights.py which can be run on any Raspberry Pi Pico, with appropriate external circuit. For a web based version you will need a Raspberry Pi Pico W with the web-lights.py program. For the network connection you should create a file secrets.py with details of your SSID and PASSWORD. The example below shows the formatting for the secrets.py file.

    SSID="NetworkSSID"
    PASSWORD="WiFiPassword"
    
## Running on startup

For the code to run automatically on start-up save the appropriate file (simple-lights.py or web-lights.py) to your Pico as main.py.


# Printed Circuit Board

The design files for the PCB are included in the folder pcb-design. This includes a zip of the gerber files which are exported for JLCPCB. Other manufacturers may need the files to be in a different format.

For further details of the printed circuit board see [PenguinTutor Pico Lights Board](https://www.penguintutor.com/projects/pico-lights) 
