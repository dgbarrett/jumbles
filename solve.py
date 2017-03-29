from process import extractWordClues
from pytesseract import image_to_string
from PIL import Image
from JumbleAnswerTemplate import JumbleAnswerTemplate

def getImageStrings(path):
	filenames, delta = extractWordClues(path)
	imgStrings = []
	for file in filenames:
		string = image_to_string(Image.open(file))
		imgStrings.append(string.replace(" ", "").lower())

	return imgStrings

def getUnJumbledWords(path):
	imgStrings = getImageStrings(path)
	wordSets = { imgString:[] for imgString in imgStrings }

	with open("dict/dict.txt","r") as fp:
		for line in fp:
			word = line.strip()
			for string in imgStrings:
				if len(word) == len(string):
					if isMatchFor(string, word):
						wordSets[string].append(word)
	return wordSets

def isMatchFor(jumble, word):
	return ''.join(sorted(jumble)) == ''.join(sorted(word))

def createFinalAnswerTemplate(wordsets):
	template = JumbleAnswerTemplate("data/j3_cropped.xls")

	for i, dictentry in enumerate(wordsets.items()):
		string = dictentry[0]
		words = dictentry[1]

		if len(words) == 1:
			template.clueAnswerTemplates[i].setWord(words[0])

	for templ in template.clueAnswerTemplates:
		print(templ.answer)
		print(templ.getSpecialLetters())

for i in [1,2,3,4,5,6,7,8,9,10][2:3]:
	wordset = getUnJumbledWords("images/j{}.png".format(i))
	createFinalAnswerTemplate(wordset)

	# for string, words in wordset.items():
	# 	print(string, words)

	# print()

