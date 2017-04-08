from load import getPixels, getImage
from lines import CompoundLine
from line_processing import (findSignificantHorizontalLines,
							 getNumberOfWordsInAnswer,
							 getAnswerHeight,
							 getClueEndPoint,
							 getAnswerStartPoint,
							 getFirstClueHeight,
							 buildCompoundLines,
							 getWordRegions)
from image_processing import extractImageArea, cropImage
from JumbleAnswerTemplate import JumbleAnswerTemplate
from pytesseract import image_to_string
from jumble_solving import solveClues
from itertools import permutations

'''
Take in an image path, crop the bullshit out of the image, and save the cropped image.
'''
def step1(filename):
	filenameNoExt = filename.split(".")[-2]
	path = "images/{}".format(filename)
	savepath = "images/{}_cropped.png".format(filenameNoExt)

	# Get image pixels and size.
	pixels = getPixels(path)
	height = len(pixels)
	width = len(pixels[0])

	print("Starting STEP 1.")
	print("\tCleaning up image for particle analysis and text extraction...")

	lines = findSignificantHorizontalLines(pixels)

	# The number of words in the answer
	wordsInAnswer = getNumberOfWordsInAnswer(lines)
	# answerTop is the y position of the top of the answer area
	# answerTop is the y position of the bottom of the answer area
	answerTop, answerBottom = getAnswerHeight(lines, wordsInAnswer)
	# Get the x position where the clues end.
	clueEndPoint = getClueEndPoint(lines, answerTop)
	# Get leftmost x position of the answer entry.
	answerStartPoint = getAnswerStartPoint(lines, wordsInAnswer)

	# Top edge of the image in line with where the clues end.
	croppoint1 = (clueEndPoint + 1, 0)
	# Point right above the answer, all the way to the right side of the image.
	croppoint2 = (width, answerTop - 1)

	# Crop the comic and associated text out.
	print("\t\tCropping comic area out of the image.")
	cropImage(path, croppoint1, croppoint2, savepath)

	# Left edge of image right below answer.
	croppoint3 = (0, answerBottom + 1)
	# Bottom right corner of image.
	croppoint4 = (width, height)

	# Crop nonsense below the answer entry.
	print("\t\tCropping area below answer entry.")
	cropImage(savepath, croppoint3, croppoint4)

	# Now that image is cleaned up, we re-find the sig horizontal lines incase there was error before.
	pixels = getPixels(savepath)
	lines = findSignificantHorizontalLines(pixels)
	# Y position of the top of the first clue.
	firstWordHeight = getFirstClueHeight(lines)

	croppoint7 = (0,0)
	croppoint8 = (clueEndPoint, firstWordHeight - 1)
	
	# Crop out area above first clue.
	print("\t\tCropping area above first clue.")
	cropImage(savepath, croppoint7, croppoint8)

	compoundLines = buildCompoundLines(lines)
	delta = (0.6 * (compoundLines[1].minY - compoundLines[0].maxY))/2

	print("\tDone cleaning. Cropped image saved at \"{}\"".format(savepath))
	print("\t\t delta = {}px".format(delta))

'''
	Function: step2A
		Take in a path to an image.  Based on the name it locates the particle 
		data extracted from jx_cropped.png by the ImageJ macro and parses it to
		create an answer template for the word jumble.
'''
def step2A(filename):
	filenameNoExt = filename.split(".")[-2]
	datafilePath = "data/{}_cropped.xls".format(filenameNoExt)

	return JumbleAnswerTemplate(datafilePath)

'''
	Function: step2B
		Take in a path to a cropped image, and return a list of character
		sequences that make up the clues.
'''
def step2B(filename):
	filenameNoExt = filename.split(".")[-2]
	path = "images/{}_cropped.png".format(filenameNoExt) 

	pixels = getPixels(path)

	lines = findSignificantHorizontalLines(pixels);
	compoundLines = buildCompoundLines(lines)

	delta = (0.6 * (compoundLines[1].minY - compoundLines[0].maxY))/2

	textCropPoints = getWordRegions(compoundLines)

	wordImages = []
	name = path.split(".")[0]
	for i, cropPointPair in enumerate(textCropPoints):
		savepath = "{}_word{}.png".format(name, i)
		wordImages.append(savepath)
		extractImageArea(path, cropPointPair[0], cropPointPair[1], savepath)

	imgStrings = []
	for file in wordImages:
		string = image_to_string(getImage(file))
		imgStrings.append(string.replace(" ", "").lower())

	return imgStrings

'''
	Function: step3
		Solve the word jumble.
'''
def step3(filename):
	answerTemplate = step2A(filename)
	clueStrings = step2B(filename)

	possabilityDict = solveClues(clueStrings);

	for i, possWords in enumerate(list(possabilityDict.values())):
		answerTemplate.addAnswer(i, possWords[0])

	jumbledCompleteAnswer = answerTemplate.getAnswerLetters()
	answerFormat = answerTemplate.getAnswerFormat()

	print(answerFormat)

	# perms = set([''.join(p) for p in permutations(jumbledCompleteAnswer)])

	# print(len(perms))

step1("j1.png")


