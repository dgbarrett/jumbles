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
            if (pixeldata[j,i] == 255):
                row += [1]
            else:
                row += [0]
        pixels += [row]

    return pixels

def getRawPixels(path):
    return Image.open(path)

def getImage(path):
    return Image.open(path)



