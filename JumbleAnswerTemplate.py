import math

class JumbleAnswerTemplate(object):
	def __init__(self, path):
		datarows = []
		with open(path, "r") as datafile:
			lines = datafile.readlines()

			for line in lines[1:]:
				row = [float(s) for s in line.split('\t')]

				if row[5] <= 1.05:
					datarows.append(row)

		answerLetterMap = [ isAnswerLetter(row[4]) for row in datarows ]
		
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

		for a,b in zip(answerLetterMap, datarows):
			print(a,b)

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

		if len(ans) > 0:
			for i, isSpecialLetter in enumerate(self.specialLetters):
				if isSpecialLetter and len(ans) > i:
					special += ans[i]
		return special	

	def __len__(self):
		return len(self.specialLetters)


def isAnswerLetter(circularity):
	return circularity >= 0.89 and circularity <= 0.94

