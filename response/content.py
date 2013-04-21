# platopus content add/suggestion script
# handles user content suggestions and adding content

from time import time;

# 0 = section name, 1 = category name, 2 = file name, 3 = req'd characters, 4 = format example, 5 = sorted
CONTENT_SECTIONS = [
["rsg/n","RSG noun",os.path.join("rsg","wordbank","nouns.txt"),[("|",1),],"singular|plural (eg: man|men or truck|trucks)",1],
["rsg/v","RSG non-transitional verb",os.path.join("rsg","wordbank","verb.txt"),[("|",4),],"verb|verbing|verbed|verben|verbs (eg: jump|jumping|jumped|jumped|jumps or strike|striking|struck|stricken|strikes)",1],
["rsg/s","RSG sentence",os.path.join("rsg","wordbank","sentences.txt"),[],"rsg sentence format (as it was entered into rsg)",0],
];

SUGGESTION_FILE = os.path.join("misc","suggestions.txt");

command = command.split(" ",1);

if (command[0] == "suggest"):
	if (user.isLoggedIn()):
		if (len(command) >= 2):
			command = command[1].split(" ",1);
			if (len(command) >= 2):
				command[0] = command[0].lower();
				foundContent = 0;
				contentGood = None;
				contentFile = None;
				for contentType in CONTENT_SECTIONS:
					if (contentType[0] == command[0]):
						contentGood = contentType;
						foundContent = 1;
						# alright, content type match... now check req'd chars...
						for requiredChar in contentType[3]:
							if (command[1].count(requiredChar[0]) != requiredChar[1]):
								self.connection.sendMsg(self.getRecipient(user,channel),"Invalid format for "+contentType[1]+". Requires content in this form: "+contentType[4]);
								contentGood = None;
								break;
						if (contentGood != None):
							contentFile = self.fileSystem.getFileContents(contentGood[2]);
							if (contentFile == None):
								contentFile = [];
							for line in contentFile:
								if (line.lower() == command[1].lower()):
									self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+"Your "+contentType[1]+" suggestion is already in the list.");
									contentGood = None;
									break;
						if (contentGood != None):
							suggestionFile = self.fileSystem.getFileContents(SUGGESTION_FILE);
							if (suggestionFile == None):
								suggestionFile = [];
							for line in suggestionFile:
								
						break;
				if (not foundContent):
					self.connection.sendMsg(self.getRecipient(user,channel),"Invalid content category '"+command[0]+"'. For a list of valid categories, see http://platopus.senselesspoliticalramblings.com/commands.html");
				elif (contentGood != None):
					# everything is good, now submit the content
					if (user.loginUserLevel >= 2):
						# elder or something
						if (contentFile == None):
							contentFile = [];
						contentFile.append(command[1]);
						if (contentGood[5]):
							contentFile.sort(key=str.lower);
						self.fileSystem.files[contentGood[2]] = contentFile;
						self.fileSystem.save(contentGood[2]);
						self.connection.sendMsg(self.getRecipient(user,channel),"Thanks for your "+contentGood[1]+" content, "+user.getIdentity()+"! It has been added.");
						user.addPoints(10);
					else:
						# plebe
						if (suggestionFile == None):
							suggestionFile = [];
						suggestionFile.append(str(int(time()))+" "+user.loginUsername+" "+contentGood[0]+" "+command[1]);
						self.fileSystem.files[SUGGESTION_FILE] = suggestionFile;
						self.fileSystem.save(SUGGESTION_FILE);
						self.connection.sendMsg(self.getRecipient(user,channel),"Thanks for your "+contentGood[1]+" suggestion, "+user.getIdentity()+"! It has been added to the suggestion file for further review. If it is accepted, you will get 20 free points!!!!");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),"Usage: suggest [category] [content]"); 
		else:
			self.connection.sendMsg(self.getRecipient(user,channel),"Usage: suggest [category] [content]"); 
	else:
		self.connection.sendMsg(self.getRecipient(user,channel),"You are not logged in and cannot suggest content. To login, use /msg "+self.connection.currentNick+" login. To create an account, use /msg "+self.connection.currentNick+" createaccount.");