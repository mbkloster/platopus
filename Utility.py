########################################
# platopus utility functions
########################################
#
# Defines basic utilities, like string merging.
#

import random;

def strMerge(wordList, mergeChar = " "):
	""" Merges a split string. """
	finalStr = "";
	for i in range(0, len(wordList)):
		if (i > 0):
			finalStr += mergeChar;
		finalStr += wordList[i];
	return finalStr;

def strPart(string, startingPoint):
	""" Grabs a split string from a certain starting point onwards. """
	if (startingPoint <= 0):
		return string;
	else:
		string = string.split(" ",startingPoint);
		if (len(string) <= startingPoint):
			return "";
		else:
			return string[startingPoint];

def getSuffix(string, lowerString, prefix):
	""" Takes a string and sees if it starts with (case insensitive) prefix + a space, and if it does, return everything thereafter. If not, return None """

	if (lowerString.startswith(prefix+" ")):
		return string[len(prefix)+1:];
	elif (lowerString == prefix):
		return "";
	else:
		return None;

def getSuffixFromList(string, lowerString, prefixList):
	for prefix in prefixList:
		suffix = getSuffix(string, lowerString, prefix);
		if (suffix != None):
			return [prefix, suffix];
	return None;

def normalize(probabilities):
	""" Normalizes a list of probabilities so sigma = 1 """
	sigma = 0;
	for i in range(0,len(probabilities)):
		if (probabilities[i] < 0):
			probabilities[i] = 0;
		elif (probabilities[i] > 1):
			probabilities[i] = 1;
		sigma += probabilities[i];
	
	if (sigma > 1):
		decreaseBy = (float(sigma) - 1)/len(probabilities);
		for i in range(0,len(probabilities)):
			probabilities[i] -= decreaseBy;
	elif (sigma < 1):
		increaseBy = (1-float(sigma))/len(probabilities);
		for i in range(0,len(probabilities)):
			probabilities[i] += increaseBy;
	return probabilities;

def getOutcome(probabilities):
	""" Grab an outcome index from a list - assume it's already been normalized... """
	outcome = random.random();
	for i in range(0,len(probabilities)-1):
		if (i > 0):
			probabilities[i] += probabilities[i-1];
		if (outcome < probabilities[i]):
			return i;
	return len(probabilities)-1;
	
def toFormattedTime(time):
	result = "";
	if (time < 0):
		result += "-";
		time *= -1;
	
	if (time > 604800):
		result += str(time/604800)+"w";
		time %= 604800;
	if (time > 86400):
		result += str(time/86400)+"d";
		time %= 86400;
	if (time > 3600):
		result += str(time/3600)+"h";
		time %= 3600;
	if (time > 60):
		result += str(time/60)+"m";
		time %= 60;
	if (time > 0 or result == ""):
		result += str(time)+"s";
	return result;

def fromFormattedTime(time):
	result = 0;
	time = time.replace(" ","").lower();
	time = time.replace("-","");
	time = time.replace("_","");
	time = time.replace("weeks","w");
	time = time.replace("week","w");
	time = time.replace("wks","w");
	time = time.replace("days","d");
	time = time.replace("day","d");
	time = time.replace("hours","h");
	time = time.replace("hour","h");
	time = time.replace("hrs","h");
	time = time.replace("hr","h");
	time = time.replace("minutes","m");
	time = time.replace("minute","m");
	time = time.replace("mins","m");
	time = time.replace("min","m");
	time = time.replace("seconds","s");
	time = time.replace("second","s");
	time = time.replace("secs","s");
	time = time.replace("sec","s");
	currentTimeSegment = "";
	if (time[-1:] != "s" and time[-1:] != "m" and time[-1:] != "h" and time[-1:] != "d" and time[-1:] != "w"):
		time += "s";
	for c in time:
		try:
			if (c == "w"):
				result += int(currentTimeSegment)*604800;
				currentTimeSegment = "";
			elif (c == "d"):
				result += int(currentTimeSegment)*86400;
				currentTimeSegment = "";
			elif (c == "h"):
				result += int(currentTimeSegment)*3600;
				currentTimeSegment = "";
			elif (c == "m"):
				result += int(currentTimeSegment)*60;
				currentTimeSegment = "";
			elif (c == "s"):
				result += int(currentTimeSegment);
				currentTimeSegment = "";
			else:
				currentTimeSegment += c;
		except ValueError:
			return 0;
	return result;

def wildcardHostname(hostname, unwildcardedNums = 3):
	# converts hostnames into wildcarded hostnames
	numbersEncountered = 0;
	numberBegin = -1;
	i = 0;
	while (i < len(hostname)):
		c = hostname[i];
		if (numberBegin < 0):
			if (c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" or c == "0"):
				numberBegin = i;
		else:
			if (c == "1" or c == "2" or c == "3" or c == "4" or c == "5" or c == "6" or c == "7" or c == "8" or c == "9" or c == "0"):
				pass;
			else:
				if (numbersEncountered >= unwildcardedNums):
					difference = i-numberBegin;
					hostname = hostname[0:numberBegin] + "*" + hostname[i:];
					i -= difference;
				numberBegin = -1;
				numbersEncountered += 1;
		i += 1;
	if (numberBegin >= 0):
		hostname = hostname[0:numberBegin]+"*";
	return hostname;

def capitalize(string):
	WHITESPACE_CHARS = "()[]{}<>.,-_+=|\?/~!@#$%^&*` ";
	newString = "";
	for i in range(0,len(string)):
		if (not WHITESPACE_CHARS.count(string[i])):
			newString += string[i].upper()+string[i+1:];
			break;
		else:
			newString += string[i];
	return newString;

def titleCapitalize(string):
	WHITESPACE_CHARS = "()[]{}<>.,-_+=|\?/~!@#$%^&*` ";
	encounteredWhitespace = 1;
	newString = "";
	for i in range(0,len(string)):
		if (encounteredWhitespace and not WHITESPACE_CHARS.count(string[i])):
			newString += string[i].upper();
			encounteredWhitespace = 0;
		elif (WHITESPACE_CHARS.count(string[i])):
			newString += string[i];
			encounteredWhitespace = 1;
		else:
			newString += string[i];
	return newString;