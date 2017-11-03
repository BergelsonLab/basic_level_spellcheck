import csv
import pandas
import distance

def spellcheck(file, n):
	wordlist = getList(n)
	hasBasic, isAudio = clean(file)

	df = pd.read_csv(file, header = 0, keep_default_na=False)

	if "word" in list(df):
		errorList = getError(df, "word", "basic_level", wordlist)
	else:
		errorList = getError(df, "labeled_object.object", "labeled_object.basic_level", wordlist)
	


def getError(df, objectC, basicC, wordlist):
	errorList = []
	for row in range(0, len(df.index)):
		word = df.get_value(row, objectC)
		if not hasMatch(word, wordlist):
			errorList.append([row+2, word])
		word = df.get_value(row, basicC)
		if not hasMatch(word, wordlist):
			errorList.append([row+2, word])

	return errorList

def getList(n):
	freqFile = "word_freq.csv"
	wordlist = []
	with open(freqFile, 'rU') as readfile:
		reader = csv.reader(readfile)
		for row in reader:
			for word in row[0:n]:
				if "+" in word:
					wordlist.extend([s.lower().replace(" ", "") for s in word.split("+")])
				else:
					word.append(word.lower().replace(" ", ""))

	return wordlist

def hasMatch(word, wordlist):
	word = word.lower().replace(" ", "")
	minDis = float("inf")

	for item in wordlist:
		dis = distance.levenshtein(word, item)
		minDis = min(dis, maxDis)

	return minDis == 0


def clean(file):
	rowlist = []
	hasBasic = True
	isAudio = True
	with open(file, 'rU') as readfile:
		reader = csv.reader(readfile)
		rowlist = [l for l in reader]
		for row in rowlist:
			if row[-1] == "":
				del row[-1]
		if "basic_level" not in rowlist[0] and "labeled_object.basic_level" not in rowlist[0]:
			hasBasic = False
			if not "word" in rowlist[0]:
				isAudio = False

	with open(file, 'wb') as writefile:
		writer = csv.writer(writefile)
		for n in rowlist:
			writer.writerow(n)

	return hasBasic, isAudio