# pico-lights
Raspberry Pi Pico LED Light Controller

Controls LED low-voltage lighting using a Raspberry Pi Pico and the Pico Lights Board.

# Code

There are three different programs included. The basic program is simple-lights.py which can be run on any Raspberry Pi Pico, with an appropriate external circuit. 
For a web based version you will need a Raspberry Pi Pico W with the web-lights.py program. Or the web-lights-twinkle.py also adds support for flashing or twinkling lights, ideal for Christmas. 

For the network versions you also need a file named secrets.py with details of your SSID and PASSWORD. The example below shows the formatting for the secrets.py file.

    SSID="NetworkSSID"
    PASSWORD="WiFiPassword"

For the web versions you should also upload the public folder and the file url_handler.py. These can be transferred using the Thonny editor.

## Running on startup

For the code to run automatically on start-up save the appropriate file (simple-lights.py, web-lights.py or web-lights-twinkle.py) to your Pico as main.py.


# Printed Circuit Board

The design files for the PCB are included in the folder pcb-design. This includes a zip of the gerber files which are exported for JLCPCB. Other manufacturers may need the files to be in a different format.

For further details of the printed circuit board see [PenguinTutor Pico Lights Board](https://www.penguintutor.com/projects/pico-lights) 
