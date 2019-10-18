import eel

eel.init('web')

@eel.expose
def hexToRgb(hex):
    hex = hex.lstrip('#')
    hlen = len(hex)
    print( tuple(int(hex[i:i+2], 16) for i in (0, 2, 4)))

eel.start('main.html')

