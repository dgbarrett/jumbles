from lines import Point, Line, CompoundLine

''' 
	Function: findSingificantHorizontalLines
		Locates the horizontal lines in the image represented by pixels which 
		are at least significance * IMG_WIDTH long. 
'''
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

'''
	Function: getNumberofWordsInAnswer
		Returns the number of words in the final answer.
		Does so by counting the number of lines at the lowest y height where 
		lines are present (each line corresponds to one word).
'''
def getNumberOfWordsInAnswer(lines):
	ylock = -1
	for i, line in enumerate(reversed(lines)):
		if i == 0:
			ylock = line.start.y
		elif line.start.y != ylock:
			return i;

	return -1

'''
	Function: getAnswerHeight
		Returns a tuple containing the max and min y values for the box where 
		the final answer is written.
'''
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

'''
	Function: getClueEndPoint
		Returns the x value where the clues end.
'''
def getClueEndPoint(lines, answerHeight):
	prevWidth = lines[0].end.x;
	for line in lines[1:]:
		if line.start.y == answerHeight:
			return prevWidth
		prevWidth = line.end.x;
	return -1

'''	
	Function: getAnswerStartPoint
		Returns the x location where the answer entry starts/
'''
def getAnswerStartPoint(lines, wordsInAnswer):
	return lines[-wordsInAnswer].start.x

'''
	Function: getFirstClueHeight
		Returns the height of the first clue.
'''
def getFirstClueHeight(lines):
	return lines[0].start.y;

'''
	Function: buildCompoundLines
		Group lines of the same length at y offsets of one into one line.

		ex
			________________
			________________
			________________

			three lines like such would be grouped into one thicker line.
'''
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

'''
	Function: getWordRegions
		Find the corner points of the area enclosing a text clue so it can be extracted.
'''
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