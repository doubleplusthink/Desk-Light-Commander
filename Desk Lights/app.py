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

theloop = ''
loopIncrementor = 0

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
    global loopIncrementor
    loopIncrementor += 1
    writeHex(color)

@eel.expose
def pulse(colors):
    global loopIncrementor
    loopIncrementor += 1
    theloop = lightLoop(loopIncrementor)
    theloop.pulse(colors)

@eel.expose
def fade(colors):
    global loopIncrementor
    loopIncrementor += 1
    theloop = lightLoop(loopIncrementor)
    theloop.fade(colors)

class lightLoop:
    def __init__(self, name):
        self.name = name
        self.running = True

    def pulse(self, colors):
        while self.running:
            for c in colors:
                if self.name < loopIncrementor:
                    self.running = False
                if self.running:
                    writeHex(c)
                    eel.sleep(0.7)

    def fade(self, colors):
        while self.running:
            for c in colors:
                if self.name < loopIncrementor:
                    self.running = False
                if self.running:
                    writeHex(c)
                    eel.sleep(0.7)

eel.start('main.html')
