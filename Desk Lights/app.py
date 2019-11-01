import eel

try:
    from pyfirmata import Arduino, util
except:
    from pip._internal import main as pipmain
    pipmain(['install','pyfirmata'])
    from pyfirmata import Arduino, util

    #Get Operating System Type
import platform
currentOs = platform.system()
if "linux" in currentOs.lower():
    currentOs = "linux"
if "windows" in currentOs.lower():
    currentOs = "windows"


    #Automatically get the port that the Arduino is on and setup the board
port = ""
if currentOs == "linux":
    import os
    feedback = "/dev/" + os.popen("ls /dev/ | grep ttyACM").read().strip()
    if len(feedback) > 11:
        port = feedback

elif currentOs == "windows":
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        p = str(p)
        if "Arduino" in p:
            port = p.split(' ', 1)[0]
            break

board=Arduino(port)

    #Set up pins
red = board.get_pin('d:3:p')
green = board.get_pin('d:5:p')
blue = board.get_pin('d:6:p')

commonAnode = True # set this to false for common cathode setup

theloop = ''
loopIncrementor = 0

    #Start the web interface
eel.init('web')

def hexToRgb(hex):
    hex = str(hex).lstrip('#')
    hlen = len(hex)
    return(tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

def writeRgb(r,g,b):
    if commonAnode:
        r = 1 - r
        g = 1 - g
        b = 1 - b
    red.write(r)
    green.write(g)
    blue.write(b)

def writeHex(hex):
    myhex = hexToRgb(hex)
    writeRgb(myhex[0]/255,myhex[1]/255,myhex[2]/255)

    #Turn off LEDs to begin with
if commonAnode:
    writeRgb(0,0,0)
else:
    writeRgb(1,1,1)

def getSteps(hex,steps):
    if type(hex) is list:
        rgb = hex
    elif type(hex) is tuple:
        rgb = list(hex)
    else:
        rgb = list(hexToRgb(hex))
    for i in range(3):
        rgb.append(rgb[0]/255/steps)
        rgb.pop(0)
    return(rgb)

def writeColorPct(color, pct):
    rgb = list(hexToRgb(color))
    for i in range(3):
        rgb[i] = rgb[i] * pct / 100
    writeRgb(rgb[0],rgb[1],rgb[2])

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

@eel.expose
def lightning(color):
    global loopIncrementor
    loopIncrementor += 1
    theloop = lightLoop(loopIncrementor)
    theloop.lightning(color)

@eel.expose
def neon(color):
    global loopIncrementor
    loopIncrementor += 1
    theloop = lightLoop(loopIncrementor)
    theloop.neon(color)

class lightLoop:
    def __init__(self, name):
        self.name = name
        self.running = True

    def pulse(self, colors):
        while self.running:
            for c in colors:
                toWrite = [0,0,0]
                increasing = True
                steps = getSteps(c,255)
                pulseIncrementor = 0

                while (increasing == True):
                    for i in range(3):
                        toWrite[i] = toWrite[i] + steps[i]
                        if toWrite[i] > 255:
                            toWrite[i] = 255
                    pulseIncrementor += 1
                    if self.name < loopIncrementor:
                        self.running = False
                    if self.running == True:
                        writeRgb(toWrite[0],toWrite[1],toWrite[2])
                        eel.sleep(0.01)
                    else:pass
                    if pulseIncrementor >= 255:
                        eel.sleep(1.0)
                        increasing = False

                while increasing == False:
                    for i in range(3):
                        toWrite[i] = toWrite[i] - steps[i]
                        if toWrite[i] <= 0:
                            toWrite[i] = 0
                    pulseIncrementor -= 1
                    if self.name < loopIncrementor:
                        self.running = False
                    if self.running == True:
                        writeRgb(toWrite[0],toWrite[1],toWrite[2])
                        eel.sleep(0.01)
                    else: pass
                    if pulseIncrementor <= 0:
                        increasing = True


    def fade(self, colors):
        currentColor = [0,0,0]
        while self.running:
            for c in colors:
                toWrite = list(currentColor)
                goto = list(hexToRgb(c))
                for i in range(3):
                    goto[i] = goto[i] - toWrite[i]
                steps = goto
                for i in range(3):
                    steps[i] /= 255 #put steps in decimal form
                    toWrite[i] /= 255 #put toWrite in decimal form
                    steps[i] /= 255 #break steps into 255 steps
                pulseIncrementor = 0
                increasing = True

                while (increasing == True):
                    for i in range(3):
                        toWrite[i] += steps[i]
                        if toWrite[i] > 1:
                            toWrite[i] = 1
                        elif toWrite[i] < 0:
                            toWrite[i] = 0
                    pulseIncrementor += 1
                    if self.name < loopIncrementor:
                        self.running = False
                    if self.running == True:
                        writeRgb(toWrite[0],toWrite[1],toWrite[2])
                        eel.sleep(0.02)
                    else:pass
                    if pulseIncrementor >= 255:
                        eel.sleep(1.0)
                        increasing = False
                        currentColor = list(hexToRgb(c))

    def lightning(self, color):
        while self.running:
            if self.name < loopIncrementor:
                self.running = False
            if self.running:
                writeHex(color)

    def neon(self, color):
        while self.running:
            if self.name < loopIncrementor:
                self.running = False
            if self.running:
                writeHex(color)

eel.start('main.html')
