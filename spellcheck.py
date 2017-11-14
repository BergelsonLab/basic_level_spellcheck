import csv
import pandas as pd
import codecheck
import sys
import os

#check spelling in basic_level and word/obejct column and print out error log csv
def check(file, n):
	hasBasic, isAudio = clean(file)

	df = pd.read_csv(file, header = 0, keep_default_na=False)

	errorList = getError(df, hasBasic, isAudio, n)

	logPath = newpath(file, isAudio)

	with open(logPath, 'wb') as writefile:
		writer = csv.writer(writefile)
		for n in errorList:
			writer.writerow(n)

	printError(errorList, logPath)

#print out error msg to terminal 
def printError(errorlist, logPath):
	asterisk = "********************************************************************"
	nl = "\n"
	alert = nl + asterisk + nl + asterisk + nl 
	errorCount = len(errorlist)

	errorMsgP = nl + repr(errorCount) + " error(s) are detected in the file." + nl
	logMsg = nl + "All errors recorded in " + logPath + nl

	print alert + errorMsgP + logMsg + alert

#get errorlist
def getError(df, hasBasic, isAudio, n):
	errorList = []
	if isAudio:
		objectC = "word"
		basicC = "basic_level"
	else:
		objectC = "labeled_object.object"
		basicC = "labeled_object.basic_level"

	errorList = wordcheck(df, objectC, errorList, n)

	if hasBasic:
		errorList = wordcheck(df, basicC, errorList, n)

	return errorList

#check words in specific column
def wordcheck(df, column, errorList, n):
	for row in range(0, len(df.index)):
		word = df.get_value(row, column)
		if word.startswith("%com:"):
			continue
		if "+" in word:
			for each in word.split("+"):
				isWord, recWords = codecheck.spellcheck(each, n)
				if not isWord:
					errorList.append([row+2, each, recWords])
		else:
			isWord, recWords = codecheck.spellcheck(word, n)
			if not isWord:
				errorList.append([row+2, word, recWords])
	return errorList

#get new_file_writeTo path
def newpath(file, isAudio):
	fileName = os.path.basename(file)
	fileName = fileName.split(".")[0]
	fileName += "_spellcheck_log.csv"
	newpath = os.path.split(file)[0]
	fullName  = os.path.join(newpath, fileName)
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
	num = 10000

	#input argument from terminal 
	file = sys.argv[1]
	if len(sys.argv) >= 3:
		num = int(sys.argv[2])

	#call main merge function
	check(file, num)