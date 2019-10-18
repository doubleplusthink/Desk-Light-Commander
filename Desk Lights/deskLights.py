try:
    from pyfirmata import Arduino, util
except:
    from pip._internal import main as pipmain
    pipmain(['install','pyfirmata'])
    from pyfirmata import Arduino, util
import time

board = Arduino('COM4')

red = board.get_pin('d:3:p')
green = board.get_pin('d:5:p')
blue = board.get_pin('d:6:p')

def rgb (r,g,b):
    red.write(1-r)
    green.write(1-g)
    blue.write(1-b)

def hexToRgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def writeHex(hex):
    myhex = hexToRgb(hex)
    rgb(myhex[0]/255,myhex[1]/255,myhex[2]/255)
    
rgb(1,1,1)

#while True:
#    writeHex('#FF0000')
#    time.sleep(0.5)
#    writeHex('#F6FF00')
#    time.sleep(0.5)
#    writeHex('#46E24E')
#    time.sleep(0.5)
#    writeHex('#1C04F4')
#    time.sleep(0.5)
#    writeHex('#A500FF')
#    time.sleep(0.5)


#board.exit()
