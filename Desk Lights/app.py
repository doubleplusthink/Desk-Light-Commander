import eel

try:
    from pyfirmata import Arduino, util
except:
    from pip._internal import main as pipmain
    pipmain(['install','pyfirmata'])
    from pyfirmata import Arduino, util

    #Automatically get the port that the Arduino is on and setup the board
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
port = ""
for p in ports:
    p = str(p)
    if "Arduino" in p:
        port = p.split(' ', 1)[0]
        break
print(port)
board=Arduino(port)

    #Set up pins
red = board.get_pin('d:3:p')
green = board.get_pin('d:5:p')
blue = board.get_pin('d:6:p')

    #Start the web interface
eel.init('web')

def hexToRgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return( tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

def writeRgb(r,g,b):
    red.write(1-r)
    green.write(1-g)
    blue.write(1-b)

def writeHex(hex):
    myhex = hexToRgb(hex)
    writeRgb(myhex[0]/255,myhex[1]/255,myhex[2]/255)

writeRgb(0,0,0)

@eel.expose
def solid(color):
    writeHex(color)


eel.start('main.html')
