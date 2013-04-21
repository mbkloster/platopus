# quote archive
# manages the entire set of quote functions
from Utility import getSuffixFromList;
from time import time;

class Quote:
	def __init__(self, quoteLine):
		if (quoteLine != ""):
			quoteLine = quoteLine.split(" ",3);
			self.time = int(quoteLine[0]);
			self.submitter = quoteLine[1];
			self.author = self.unformatAuthor(quoteLine[2]);
			self.quote = quoteLine[3];
		else:
			self.time = 0;
			self.submitter = "";
			self.author = "";
			self.quote = "";
	
	@staticmethod
	def unformatAuthor(author):
		""" Converts a formatted author name into a normal-looking one. """
		newAuthor = "";
		ignoreUnderline = 0;
		for i in range(0,len(author)):
			if (author[i] == "_"):
				if (i < len(author)-1 and author[i+1] == "_"):
					newAuthor += "_";
					ignoreUnderline = 1;
				elif (not ignoreUnderline):
					newAuthor += " ";
				else:
					ignoreUnderline = 0;
			else:
				newAuthor += author[i];
		return newAuthor;
	
	@staticmethod
	def formatAuthor(author):
		""" Converts an unformatted author to a formatted one. """
		newAuthor = ""

def searchQuotes(quoteList, searchFor):
	searchFor = searchFor.lower();
	matches = [];
	for i in range(0,len(quoteList)):
		line = quoteList[i].split(" ",2);
		if (len(line) >= 3):
			line = line[2].lower();
			if (line.find(searchFor) > -1):
				matches.append(i+1);
	return matches;

command = command.split(" ",1);
if (len(command) <= 1):
	function = "intro";
	command = command[0];
	line = "";
else:
	possibleFunctions = ["search","quicksearch","get","save","random","latest","intro"];
	command = command[1];
	suffix = getSuffixFromList(command,command.lower(),possibleFunctions);
	if (suffix == None):
		try:
			if (command[0:1] == "#"):
				command2 = command[1:];
			else:
				command2 = command;
			number = int(command2);
			function = "get";
			line = str(number);
		except ValueError:
			if (len(command.strip()) > 0):
				function = "quicksearch";
				line = command;
			else:
				function = "intro";
				line = "";
	else:
		function = suffix[0];
		line = suffix[1];

quoteFile = os.path.join(".","misc","quotes.txt");
if (function == "intro"):
	self.connection.sendMsg(self.getRecipient(user,channel),"The quote archive currently has "+str(self.fileSystem.getLineCount(quoteFile))+" entries.");
elif (function == "get"):
	if (len(line) >= 2 and line[0:1] == "#"):
		line = line[1:];
	try:
		number = int(line);
	except ValueError:
		self.connection.sendMsg(self.getRecipient(user,channel),"A valid quote number is required.");
	else:
		quoteLine = self.fileSystem.getLine(quoteFile,number-1);
		if (quoteLine != ""):
			quote = Quote(quoteLine);
			self.connection.sendMsg(self.getRecipient(user,channel),"\""+quote.quote+"\" -"+quote.author+" (#"+str(number)+")");
		else:
			self.connection.sendMsg(self.getRecipient(user,channel),"Quote #"+str(number)+" not in the quote database.");
elif (function == "search"):
	quoteFileContents = self.fileSystem.getFileContents(quoteFile);
	matches = searchQuotes(quoteFileContents,line);
	if (len(matches) <= 0):
		self.connection.sendMsg(self.getRecipient(user,channel),"No matches found for "+line+" in the quote database.");
	elif (len(matches) == 1):
		quote = Quote(quoteFileContents[matches[0]-1]);
		self.connection.sendMsg(self.getRecipient(user,channel),"\""+quote.quote+"\" -"+quote.author+" (#"+str(matches[0])+" - only match)");
	else:
		matchList = "";
		for match in matches:
			matchList += " #"+str(match);
		self.connection.sendMsg(self.getRecipient(user,channel),"Matches found for "+line+":"+matchList);
elif (function == "quicksearch"):
	quoteFileContents = self.fileSystem.getFileContents(quoteFile);
	matches = searchQuotes(quoteFileContents,line);
	if (len(matches) <= 0):
		self.connection.sendMsg(self.getRecipient(user,channel),"No matches found for "+line+" in the quote database.");
	elif (len(matches) == 1):
		quote = Quote(quoteFileContents[matches[0]-1]);
		self.connection.sendMsg(self.getRecipient(user,channel),"\""+quote.quote+"\" -"+quote.author+" (#"+str(matches[0])+" - only match)");
	else:
		number = matches[self.console.random.randInt(0,len(matches))-1];
		quote = Quote(quoteFileContents[number-1]);
		self.connection.sendMsg(self.getRecipient(user,channel),"\""+quote.quote+"\" -"+quote.author+" (#"+str(number)+")");
elif (function == "latest"):
	quoteFileContents = self.fileSystem.getFileContents(quoteFile);
	quote = Quote(quoteFileContents[len(quoteFileContents)-1]);
	self.connection.sendMsg(self.getRecipient(user,channel),"\""+quote.quote+"\" -"+quote.author+" (#"+str(len(quoteFileContents))+")");
elif (function == "random"):
	quoteFileContents = self.fileSystem.getFileContents(quoteFile);
	quoteNumber = self.console.random.randInt(0,len(quoteFileContents)-1);
	quote = Quote(quoteFileContents[quoteNumber]);
	self.connection.sendMsg(self.getRecipient(user,channel),"\""+quote.quote+"\" -"+quote.author+" (#"+str(quoteNumber+1)+")");
elif (function == "save"):
	line = line.split(" ",1);
	if (len(line) >= 2):
		author = line[0];
		quote = line[1];
		quoteFileContents = self.fileSystem.getFileContents(quoteFile);
		quoteFileContents.append(str(int(time()))+" "+user.nick+" "+author+" "+quote);
		self.fileSystem.save(quoteFile,quoteFileContents);
		self.fileSystem.files[quoteFile] = quoteFileContents;
		self.connection.sendMsg(self.getRecipient(user,channel),"Quote by "+Quote.unformatAuthor(author)+" saved successfully as quote #"+str(len(quoteFileContents))+".");
		user.addPoints(20);