command = command.split(" ");
if (len(command) < 2):
	self.connection.sendMsg(self.getRecipient(user,channel),"Usage: rsgsource [rsg #]");
else:
	try:
		rsgNumber = int(command[1]);
	except ValueError:
		self.connection.sendMsg(self.getRecipient(user,channel),"Correct me if I'm wrong but \""+command[1]+"\" is not a number. I like numbers.");
	else:
		if (rsgNumber <= 0):
			self.callResponse("fuck you",0,user,channel,0);
		else:
			contents = self.fileSystem.getFileContents(os.path.join("rsg","wordbank","sentences.txt"));
			if (rsgNumber > len(contents)):
				self.connection.sendMsg(self.getRecipient(user,channel),"This rsg # seems to be beyond my "+str(len(contents))+" rsg's.");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),contents[rsgNumber-1]);