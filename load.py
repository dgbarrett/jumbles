from PIL import Image

def getPixels(path):
    im = Image.open(path) 
    width = im.size[0]
    height = im.size[1]

    pixeldata = im.load()

    pixels = []
    for i in range(height):
        row = []
        for j in range(width):
            if (pixeldata[j,i] == (255,255,255)):
                row += [0]
            else:
                row += [1]
        pixels += [row]

    return pixels

def getImage(path):
    return Image.open(path)



