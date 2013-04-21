# user login script
# handles logging in/out

from Utility import wildcardHostname;

MAX_HOSTNAMES_SAVED = 4;

def addUserHost(self, hostname, user):
	global MAX_HOSTNAMES_SAVED, wildcardHostname;
	userhosts = self.fileSystem.getFileContents(os.path.join("misc","userhosts.txt"),0);
	relevantEntries = []; # stores entries that match this user
	wildcardHost = wildcardHostname(hostname).lower();
	hostnameExists = 0;
	for i in range(0,len(userhosts)):
		entry = userhosts[i];
		entry2 = entry.split(" ");
		if (entry2[0] == wildcardHost):
			if (len(entry2) >= 2 and entry2[1].lower() != user.loginUsername.lower()):
				entry = entry2[0] + user.loginUsername;
				userhosts[i] = entry;
			hostnameExists = 1;
			relevantEntries.append(entry);
		elif (len(entry2) >= 2 and entry2[1].lower() == user.loginUsername.lower()):
			relevantEntries.append(entry);
	if (len(relevantEntries) >= MAX_HOSTNAMES_SAVED):
		userhosts.remove(relevantEntries[0]);
	if (not hostnameExists):
		userhosts.append(wildcardHost+" "+user.loginUsername);
	self.fileSystem.save(os.path.join("misc","userhosts.txt"),userhosts);

def removeUserHost(self, hostname, user):
	global MAX_HOSTNAMES_SAVED, wildcardHostname;
	userhosts = self.fileSystem.getFileContents(os.path.join("misc","userhosts.txt"),0);
	relevantEntries = []; # stores entries that match this user
	wildcardHost = wildcardHostname(hostname).lower();
	for i in range(0,len(userhosts)):
		entry = userhosts[i];
		entry2 = entry.split(" ");
		if (entry2[0] == wildcardHost):
			if (len(entry2) >= 2 and entry2[1].lower() == user.loginUsername.lower()):
				userhosts.remove(entry);
				break;
	self.fileSystem.save(os.path.join("misc","userhosts.txt"),userhosts);

if (channel == ""):
	if (parameters.has_key("logout")):
		if (user.isLoggedIn()):
			username = user.loginUsername;
			removeUserHost(self,user.host,user);
			logoutResult = user.logout();
			if (logoutResult[0]):
				self.connection.sendNotice(self.getRecipient(user,channel),"Thank you, "+username+". You have been logged out. Your account info will no longer be remembered on this computer.");
			else:
				self.connection.sendNotice(self.getRecipient(user,channel),logoutResult[1]);
		else:
			self.connection.sendNotice(self.getRecipient(user,channel),"Sorry, bro, but you're not logged in and cannot be logged out.");
	else:
		if (not user.isLoggedIn()):
			userDir = "accounts";
			components = command.split();
			if (len(components) < 3):
				self.connection.sendNotice(self.getRecipient(user,channel),"Usage: login [username] [password]");
			else:
				command = command.split(" ");
				hashedPassword = hashlib.md5(command[2]).hexdigest();
				loginResult = user.attemptLogin(command[1],hashedPassword,self.fileSystem);
				if (loginResult[0]):
					# login successful
					addUserHost(self,user.host, user);
					self.connection.sendNotice(self.getRecipient(user,channel),"You have been logged in as "+user.loginUsername+". You currently have "+str(user.availablePoints)+" points available ("+str(user.totalPoints)+" total). Your current rank is "+user.getRank()+".");
					self.connection.sendNotice(self.getRecipient(user,channel),"Your login will be automatically remembered. To show options for account settings, use the command accounthelp. To log out, use the command logout.");
				else:
					self.connection.sendNotice(self.getRecipient(user,channel),loginResult[1]);
		else:
			self.connection.sendNotice(self.getRecipient(user,channel),"You are already logged in. Use the command logout to log out.");
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"This command may only be used over a private message. You wouldn't want people seeing our personal business, would you, "+user.nick+"?");
	self.connection.sendNotice(user.nick,"Type /msg "+self.connection.currentNick+" [command] to send a private message to me.");