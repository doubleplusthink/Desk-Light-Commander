import eel

try:
    from pyfirmata import Arduino, util
except:
    from pip._internal import main as pipmain
    pipmain(['install','pyfirmata'])
    from pyfirmata import Arduino, util

board=Arduino('COM4')

red = board.get_pin('d:3:p')
green = board.get_pin('d:5:p')
blue = board.get_pin('d:6:p')

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

writeRgb(1,1,1)

@eel.expose
def solid(r,g,b):
    writeRgb(int(r)/255,int(g)/255,int(b)/255)

eel.start('main.html')

