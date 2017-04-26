def getAnswerFormat(lines):
	y = lines[-1].end.y
	answerWordLens = []

	for line in reversed(lines):
		if line.end.y == y:
			answerWordLens.append(line.magnitude)

	return list(reversed(answerWordLens))

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

def Dictionary():
	MAXLEN = 12
	with open("dict/dict.txt","r") as fp:
		dictionary = {}

		for c in range(ord('a'), ord('z')+1):
			dictionary[chr(c)] = {1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}, 7:{}, 8:{}, 9:{},10:{}, 11:{}, 12:{},13:{}, 14:{}, 15:{}}

		for line in fp:
			word = line.strip()
			wordlen = len(word)

			if ord(word[0]) in range(ord('a'), ord('z')+1) and word.isalpha() and wordlen in range(1, MAXLEN+1):
				dictionary[word[0]][wordlen][word] = True;

		return dictionary

def isMatchFor(jumble, word):
	return ''.join(sorted(jumble)) == ''.join(sorted(word))