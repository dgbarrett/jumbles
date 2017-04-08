def solveClues(imgStrings):
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