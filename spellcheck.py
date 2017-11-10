import csv
import pandas as pd
import codecheck
import re
import sys

#check spelling in basic_level and word/obejct column and print out error log csv
def check(file):
	hasBasic, isAudio = clean(file)

	df = pd.read_csv(file, header = 0, keep_default_na=False)

	errorList = getError(df, hasBasic, isAudio)

	logPath = newpath(file, isAudio)

	with open(logPath, 'wb') as writefile:
		writer = csv.writer(writefile)
		for n in errorList:
			writer.writerow(n)

#get errorlist
def getError(df, hasBasic, isAudio):
	errorList = []
	if isAudio:
		objectC = "word"
		basicC = "basic_level"
	else:
		objectC = "labeled_object.object"
		basicC = "labeled_object.basic_level"

	for row in range(0, len(df.index)):
		word = df.get_value(row, objectC)
		if "+" in word:
			for each in word.split("+"):
				isWord, recWords = codecheck.spellcheck(word)
				if not isWord:
					errorList.append([row+2, word, recWords])
		else:
			isWord, recWords = codecheck.spellcheck(word)
			if not isWord:
				errorList.append([row+2, word, recWords])
		if hasBasic:
			word = df.get_value(row, basicC)
			isWord, recWords = codecheck.spellcheck(word)
			if not isWord:
				errorList.append([row+2, word, recWords])

	return errorList


#get single file name from path
def getFileName(path):
	pathList = re.split("\\\|/", path)
	fileName = pathList[-1]
	return fileName

#combine path list into single path string
def combinePath(pathList):
	fullName = "/"
	for i in range(len(pathList)):
		if ".csv" in pathList[i] or not pathList[i]:
			continue
		fullName += pathList[i]
		fullName += "/"
	return fullName

#get new_file_writeTo path
def newpath(file, isAudio):
	fileName = getFileName(file)
	fileName = fileName.split(".")[0]
	fileName += "_spellcheck_log.csv"
	newpathList = re.split("\\\|/", file)
	fullName = combinePath(newpathList)
	fullName += fileName
	return fullName

#clean csv file for pandas dataframe reading and check file type
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
		if "basic_level" not in rowlist[0] or "labeled_object.basic_level" not in rowlist[0]:
			hasBasic = False
			if not "word" in rowlist[0]:
				isAudio = False

	with open(file, 'wb') as writefile:
		writer = csv.writer(writefile)
		for n in rowlist:
			writer.writerow(n)

	return hasBasic, isAudio

if __name__ == "__main__":

	#input argument from terminal 
	file = sys.argv[1]

	#call main merge function
	check(file)