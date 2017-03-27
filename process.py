import os
from load import getPixels, getImage
from ImageStructures import Line, Point

IMAGES_DIR = "images"
IMAGE_FILES = ["j1.jpg", "j2.jpg", "j3.jpg", "j4.jpg"]
IMAGES = [os.path.join(IMAGES_DIR, IMAGE_PATH) for IMAGE_PATH in IMAGE_FILES]

def main():
	pix = getPixels(IMAGES[0])
	findSignificantHorizontalLines(pix)

def findSignificantHorizontalLines(pixels, signifcance=0.1):
	height = len(pixels)
	width = len(pixels[0])

	line = None
	lines = []

	for y, row in enumerate(pixels):
		for x, pixel in enumerate(row):
			if line and not pixel:
				line.end = Point(x,y)

				if line.magnitude >= signifcance*width:
					lines += [line]
				line = None
			elif not line and pixel:
				line = Line( Point(x,y) )
		if line:
			line.end = Point(width-1,y)
			if line.magnitude >= signifcance*width:
				lines += [line]
			line = None

	image = getImage(IMAGES[0])
	imgpx = image.load()

	for line in lines:
		for x,y in line:
			imgpx[x,y] = (255,255,255)

	image.save("images/text.jpg")


if __name__ == "__main__":
	main()