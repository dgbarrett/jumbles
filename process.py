import os
from load import getPixels, getImage
from ImageStructures import Line, Point, CompoundLine

def extractWordClues(path):
	savepath = path.split(".")[0] + "_cropped.png"

	# Get image pixels and size.
	pixels = getPixels(path)
	height = len(pixels)
	width = len(pixels[0])

	lines = findSignificantHorizontalLines(pixels)

	# The number of words in the answer
	wordsInAnswer = getNumberOfWordsInAnswer(lines)
	# answerTop is the y position of the top of the answer area
	# answerTop is the y position of the bottom of the answer area
	answerTop, answerBottom = getAnswerHeight(lines, wordsInAnswer)
	# Get the x position where the clues end.
	clueEndPoint = getWordEndPoint(lines, answerTop)
	# Get leftmost x position of the answer entry.
	answerStartPoint = getAnswerStartPoint(lines, wordsInAnswer)

	# Top edge of the image in line with where the clues end.
	croppoint1 = (clueEndPoint + 1, 0)
	# Point right above the answer, all the way to the right side of the image.
	croppoint2 = (width, answerTop - 1)
	# Crop the comic and associated text out.
	cropImage(path, croppoint1, croppoint2, savepath)

	# Left edge of image right below answer.
	croppoint3 = (0, answerBottom + 1)
	# Bottom right corner of image.
	croppoint4 = (width, height)
	# Crop nonsense below the answer entry.
	cropImage(savepath, croppoint3, croppoint4)

	# # Left edge of image, in line with top of answer entry.
	# croppoint5 = (0, answerTop)
	# # Point just to the left of the bottom left corner of the answer entry.
	# croppoint6 = (answerStartPoint - 5, answerBottom + 5)
	# # Crop answer title (to left of answer entry).
	# cropImage(savepath, croppoint5, croppoint6)

	# Now that image is cleaned up, we re-find the sig horizontal lines incase there was error before.
	pixels = getPixels(savepath)
	lines = findSignificantHorizontalLines(pixels)
	# Y position of the top of the first clue.
	firstWordHeight = getFirstWordHeight(lines)

	croppoint7 = (0,0)
	croppoint8 = (clueEndPoint, firstWordHeight - 1)
	# Crop out area above first clue.
	cropImage(savepath, croppoint7, croppoint8)

	compoundLines = buildCompoundLines(lines)

	delta = (0.6 * (compoundLines[1].minY - compoundLines[0].maxY))/2

	textCropPoints = getWordRegions(compoundLines)

	wordImages = []
	name = path.split(".")[0]
	for i, cropPointPair in enumerate(textCropPoints):
		savepath = "{}_word{}.png".format(name, i)
		wordImages.append(savepath)
		extractImageArea(path, cropPointPair[0], cropPointPair[1], savepath)

	return wordImages, delta

def buildCompoundLines(lines):
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

	return compoundLines


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

def findSignificantHorizontalLines(pixels, signifcance=0.10):
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

def extractImageArea(path, cp1, cp2, savepath):
	im = getImage(path)
	width = im.size[0]
	height = im.size[1]

	pixeldata = im.load()
	for i in range(height):
		for j in range(width):
			if j not in range(cp1[0],cp2[0]) or i not in range(cp1[1],cp2[1]):
				pixeldata[j,i] = 0

	im.save(savepath)

def cropImage(path, cp1,cp2, savepath=None):
	if not savepath:
		savepath = path

	im = getImage(path)
	width = im.size[0]
	height = im.size[1]

	pixeldata = im.load()
	for i in range(height):
		for j in range(width):
			if j in range(cp1[0],cp2[0]) and i in range(cp1[1],cp2[1]):
				pixeldata[j,i] = 0

	im.save(savepath)
