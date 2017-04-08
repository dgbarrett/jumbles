import math
import operator

class JumbleAnswerTemplate(object):
	def __init__(self, path):
		datarows = []
		with open(path, "r") as datafile:
			lines = datafile.readlines()

			for line in lines[1:]:
				row = [float(s) for s in line.split('\t')]

				if row[5] <= 1.09:
					datarows.append(row)

		# sizes = sorted([row[1] for row in datarows])
		# maxdifIndex = getMaxDifIndex(sizes)
		# thresholdValue = (sizes[maxdifIndex] + sizes[maxdifIndex+1])/2

		# circs = sorted([row[4] for row in datarows])
		# maxdifIndex = getMaxDifIndex(circs)
		# circThreshold = (circs[maxdifIndex] + circs[maxdifIndex+1])/2

		#find the start of the words
		wordStartTemplate = [True]
		prevY = datarows[0][3]
		for row in datarows[1:]:
			if math.fabs(prevY - row[3]) > 1:
				wordStartTemplate.append(True)
			else:
				wordStartTemplate.append(False)
			prevY = row[3]

		currY = 0
		for wordstart, row in zip(wordStartTemplate, datarows):
			if wordstart:
				currY = int(row[3])
			row[3] = currY

		templist = None
		wordLists = []
		for row, newword in zip(datarows, wordStartTemplate):
			if newword:
				if templist:
					wordLists.append(templist)
				
				templist = []
			templist.append(row)

		if templist:
			wordLists.append(templist)

		datarows = []
		for lis in wordLists:
			lis = sorted(lis, key=lambda x:x[2])
			datarows += lis

		answerLetterMap = [ isAnswerLetter(row[7]) for row in datarows ]

		wordStartTemplate = [True]
		prevY = datarows[0][3]
		for row in datarows[1:]:
			if math.fabs(prevY - row[3]) > 1:
				wordStartTemplate.append(True)
			else:
				wordStartTemplate.append(False)
			prevY = row[3]

		ansTemplate = None
		self.clueAnswerTemplates = []
		for isAnsLetter, wordStart, data in zip(answerLetterMap, wordStartTemplate, datarows):
			if not ansTemplate:
				ansTemplate = TemplateWord()
			elif wordStart:
				self.clueAnswerTemplates.append(ansTemplate)
				ansTemplate = TemplateWord()

			ansTemplate.addLetter(isAnsLetter)
		self.clueAnswerTemplates.append(ansTemplate)

	def getAnswerLetters(self):
		letters = ""
		for template in self.clueAnswerTemplates:
			letters += template.getSpecialLetters()

		return letters

	def addAnswer(self, index, answer):
		self.clueAnswerTemplates[index].answer = answer

	def getAnswerFormat(self):
		answerWordLens = []
		for template in self.clueAnswerTemplates:
			if template.isAnswerTemplate():
				answerWordLens.append(len(template))

		return answerWordLens

class TemplateWord(object):
	def __init__(self):
		self.answer = ""
		self.specialLetters = []

	def addLetter(self, isAnsLetter):
		self.specialLetters.append(isAnsLetter)

	def setWord(self, answer):
		self.answer = answer

	def getSpecialLetters(self):
		ans = list(self.answer)
		special = ""

		for letter, isSpecial in zip(ans, self.specialLetters):
			if isSpecial:
				special += letter

		return special

	def isAnswerTemplate(self):
		return sum(self.specialLetters) == len(self);

	def __len__(self):
		return len(self.specialLetters)

	def __str__(self):
		st = ""
		for letter in self.specialLetters:
			st += str(letter) + " "

		return st

def isAnswerLetter(solidity):
	return int(not math.isclose(solidity, 1.00))

def getMaxDifIndex(sizes):
	maxdif = 0;
	currval = sizes[0]
	index = 0;

	for i,size in enumerate(sizes[1:]):
		dif = size - currval

		if dif > maxdif:
			index = i
			maxdif = dif

		currval = size

	return index


