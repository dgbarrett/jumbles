import os
from load import getPixels, getImage
from ImageStructures import Line, Point, CompoundLine

IMAGES_DIR = "images"
IMAGE_FILES = ["j1.jpg", "j2.jpg", "j3.jpg"]
IMAGES = [os.path.join(IMAGES_DIR, IMAGE_PATH) for IMAGE_PATH in IMAGE_FILES]

def main():
	for path in IMAGES:
		savepath = path.split(".")[0] + ".png"
		pixels = getPixels(path)
		lines = findSignificantHorizontalLines(pixels)
		wordsInAnswer = getNumberOfWordsInAnswer(lines)
		answerTop, answerBottom = getAnswerHeight(lines, wordsInAnswer)
		wordEndPoint = getWordEndPoint(lines, answerTop)
		answerStartPoint = getAnswerStartPoint(lines, wordsInAnswer)

		cp1 = (wordEndPoint+1,0)
		cp2 = (len(pixels), answerTop-1)

		cp3 = (0, answerBottom+1)
		cp4 = (len(pixels[0]), len(pixels))

		cp5 = (0, answerTop)
		cp6 = (answerStartPoint-5, answerBottom+5)

		# modifyImage(path, lines, path+".png")
		modifyImage(path, cp1,cp2, savepath)
		modifyImage(savepath,cp3,cp4,savepath)
		modifyImage(savepath,cp5,cp6,savepath)

		pixels = getPixels(savepath)
		lines = findSignificantHorizontalLines(pixels)
		firstWordHeight = getFirstWordHeight(lines)

		cp7 = (0,0)
		cp8 = (wordEndPoint,firstWordHeight - 1)

		modifyImage(savepath,cp7,cp8,savepath)

		prevY = lines[0].start.y
		count = 0
		lastnew = False
		compoundLines = []
		currCompoundLine = CompoundLine()
		currCompoundLine.add(lines[0])

		for line in lines[1:]:
			dif = line.start.y - prevY
			if dif not in range(0,8):
				count += 1
				lastnew = True
				compoundLines += [currCompoundLine]
				currCompoundLine = CompoundLine()
			else:
				currCompoundLine.add(line)
				lastnew = False

			prevY = line.start.y

		if not lastnew:
			count +=1
			compoundLines += [currCompoundLine]

		crops = getWordRegions(compoundLines)

		for i,crop in enumerate(crops):
			name = savepath.split(".")[0]
			name += "_" + str(i) + ".png"
			cropOutImageArea(path,crop[0],crop[1],name)


def getWordRegions(compoundLines):
	# Last two horizontal lines define the answer
	clines = compoundLines[:-2]
	crops = []
	cp1 = None
	cp2 = None 

	for i,line in enumerate(clines[::3]):
		nextline = clines[(i*3)+1]

		cp1 = (line.minX + 10, line.maxY + 1)
		cp2 = (line.maxX - 10, nextline.minY - 1)

		crops.append( [cp1,cp2] )

	return crops

def findSignificantHorizontalLines(pixels, signifcance=0.17):
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

	return lines

def getNumberOfWordsInAnswer(lines):
	ylock = -1
	for i, line in enumerate(reversed(lines)):
		if i == 0:
			ylock = line.start.y
		elif line.start.y != ylock:
			return i;

	return -1

def getAnswerHeight(lines, wordsInAnswer):
	answerBottom = lines[-1].start.y;
	answerTop = -1

	abOG = answerBottom

	findtop = False
	findbottom = True

	lines.reverse()

	for line in lines[wordsInAnswer::wordsInAnswer]:
		if findbottom:
			if line.start.y <= answerBottom - 1 and line.start.y >= answerBottom - 10: 
				answerBottom = line.start.y
			else:
				findbottom = False
				findtop = True
		
		if findtop:
			if answerTop == -1:
				answerTop = line.start.y
			elif line.start.y <= answerTop -1 and line.start.y >= answerTop - 10:
				answerTop = line.start.y 
			else:
				break

	lines.reverse()

	return answerTop, abOG

def getWordEndPoint(lines, answerHeight):
	prevWidth = lines[0].end.x;
	for line in lines[1:]:
		if line.start.y == answerHeight:
			return prevWidth
		prevWidth = line.end.x;
	return -1

def getAnswerStartPoint(lines,wordsInAnswer):
	return lines[-wordsInAnswer].start.x

def getFirstWordHeight(lines):
	return lines[0].start.y;

def modifyImageL(path, lines, savepath):
	image = getImage(path)
	imgpx = image.load()

	for line in lines:
		for x,y in line:
			imgpx[x,y] = (255,255,255)

	image.save(savepath)

def cropOutImageArea(path, cp1, cp2, savepath):
	im = getImage(path)
	width = im.size[0]
	height = im.size[1]

	pixeldata = im.load()
	for i in range(height):
		for j in range(width):
			if j not in range(cp1[0],cp2[0]) or i not in range(cp1[1],cp2[1]):
				pixeldata[j,i] = (255,255,255)

	im.save(savepath)


def modifyImage(path, cp1,cp2, savepath):
	im = getImage(path)
	width = im.size[0]
	height = im.size[1]

	pixeldata = im.load()
	for i in range(height):
		for j in range(width):
			if j in range(cp1[0],cp2[0]) and i in range(cp1[1],cp2[1]):
				pixeldata[j,i] = (255,255,255)

	im.save(savepath)

if __name__ == "__main__":
	main()