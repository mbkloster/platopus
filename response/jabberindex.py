# jabber index script
# takes in a line and indexes it in the right jabber channels.
# This is NOT meant to be executed by itself, but
# rather, as part of ResponseSystem.
from time import time;

if (not parameters.has_key("max_lines")):
	parameters["max_lines"] = 100;

def addNGram(nGram, line):
	""" Adds traces of a line to an existing n-gram """
	line = line.split(" ");
	for i in range(0,len(line)):
		word = line[i].lower();
		if (not nGram.has_key(word)):
			nGram[word] = [];
		
		if (i+1 < len(line)):
			nextWord = line[i+1:];
			nGram[word].append(nextWord);
		else:
			nGram[word.lower()].append([]);
	return nGram;

def removeNGram(nGram, line):
	""" Removes traces of a line from an existing n-gram """
	line = line.split(" ");
	for i in range(0,len(line)):
		word = line[i].lower();
		if (nGram.has_key(word)):
			if (i+1 < len(line)):
				nextWord = line[i+1:];
				if (nGram[word].count(nextWord) > 0):
					nGram[word].remove(nextWord);
			else:
				if (nGram[word].count([]) > 0):
					nGram[word.lower()].remove([]);
			if (len(nGram[word]) <= 0):
				del nGram[word];
	return nGram;

# first, adjust the nick jabber file
nickFileName = user.nick.lower().replace("|","_").replace("\\","_").replace("/","_");
jabberFile = self.fileSystem.getFileContents(os.path.join(".","jabber","nick",nickFileName+".txt"));
if (jabberFile == None):
	jabberFile = [];
jabberFile.append(command);

if (not self.jabberNGrams.has_key(user.nick.lower())):
	# no n-gram exists for this nick yet, so add it
	self.jabberNGrams[user.nick.lower()] = {};
	for line in jabberFile:
		self.jabberNGrams[user.nick.lower()] = addNGram(self.jabberNGrams[user.nick.lower()], line);
else:
	# n-gram exists, so add this line
	self.jabberNGrams[user.nick.lower()] = addNGram(self.jabberNGrams[user.nick.lower()], command);

if (len(jabberFile) > parameters["max_lines"]):
	if (self.jabberNGrams.has_key(user.nick.lower())):
		self.jabberNGrams[user.nick.lower()] = removeNGram(self.jabberNGrams[user.nick.lower()],jabberFile[0]);
	jabberFile = jabberFile[1:];

# SAVE
self.fileSystem.save(os.path.join(".","jabber","nick",nickFileName+".txt"),jabberFile);

# now, adjust the channel jabber file
channelFileName = channel.lower().replace("|","_").replace("\\","_").replace("/","_");
jabberFile = self.fileSystem.getFileContents(os.path.join(".","jabber","nick",channelFileName+".txt"));
if (jabberFile == None):
	jabberFile = [];
jabberFile.append(command);

if (not self.jabberNGrams.has_key(channel.lower())):
	# no n-gram exists for this channel yet, so add it
	self.jabberNGrams[channel.lower()] = {};
	for line in jabberFile:
		self.jabberNGrams[channel.lower()] = addNGram(self.jabberNGrams[channel.lower()], line);
else:
	# n-gram exists, so add this line
	self.jabberNGrams[channel.lower()] = addNGram(self.jabberNGrams[channel.lower()], command);

if (len(jabberFile) > parameters["max_lines"]):
	if (self.jabberNGrams.has_key(channel.lower())):
		self.jabberNGrams[channel.lower()] = removeNGram(self.jabberNGrams[channel.lower()],jabberFile[0]);
	jabberFile = jabberFile[1:];

# SAVE
self.fileSystem.save(os.path.join(".","jabber","nick",channelFileName+".txt"),jabberFile);

# now, if necessary, adjust the account file
if (user.isLoggedIn()):
	accountFileName = user.loginUsername.lower().replace("|","_").replace("\\","_").replace("/","_");
	jabberFile = self.fileSystem.getFileContents(os.path.join(".","jabber","account",accountFileName+".txt"));
	if (jabberFile == None):
		jabberFile = [];
	jabberFile.append(command);
	
	if (not self.jabberNGrams.has_key("account "+user.loginUsername.lower())):
		# no n-gram exists for this account yet, so add it
		self.jabberNGrams["account "+user.loginUsername.lower()] = {};
		for line in jabberFile:
			self.jabberNGrams["account "+user.loginUsername.lower()] = addNGram(self.jabberNGrams["account "+user.loginUsername.lower()], line);
	else:
		self.jabberNGrams["account "+user.loginUsername.lower()] = addNGram(self.jabberNGrams["account "+user.loginUsername.lower()], command);
	
	if (len(jabberFile) > parameters["max_lines"]):
		if (self.jabberNGrams.has_key("account "+user.loginUsername.lower())):
			self.jabberNGrams["account "+user.loginUsername.lower()] = removeNGram(self.jabberNGrams[channel.lower()],jabberFile[0]);
		jabberFile = jabberFile[1:];

	# SAVE
	self.fileSystem.save(os.path.join(".","jabber","account",accountFileName+".txt"),jabberFile);

# now go through the existing n-grams and delete any any all unnecessary ones
for nGram, contents in self.jabberNGrams.items():
	if (not self.fileSystem.files.has_key(os.path.join(".","jabber","nick",nGram+".txt"))):
		del self.jabberNGrams[nGram];

# now check for the RANDOM KICKER
if (self.console.getVar("rankick_target") != "" and self.console.getVar("rankick_chance") > 0 and self.console.getVar("rankick_channel") != "" and self.console.getVar("rankick_channel") == channel):
	if (random.random() < self.console.getVar("rankick_chance")):
		self.connection.kickUser(self.console.getVar("rankick_channel"),self.console.getVar("rankick_target"),command);