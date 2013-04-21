# platopus account creation script
# creates new accounts... as you might expect
#
# Account lines are in this format:
# 0: the account username (including case)
# 1: password (md5'd)
# 2: reg timestamp
# 3: last login timestamp
# 4: cumulative points
# 5: available points
# 6: user level (1-3)
# 7: email
# 8: real name
# 9: location
# 10: tagline
# 11: gender (m/f/n)
# 12: registration nick/ident/host

from time import time;

MIN_PASSWORD_LENGTH = 6;
MIN_USERNAME_LENGTH = 2;
MAX_USERNAME_LENGTH = 15;
USERNAME_DISALLOWED_CHARS = "{}<>:;\"'!@#$%^&*-.,";
DISALLOWED_USERNAMES = ["me","platopus"];

if (channel == ""):
	if (not user.isLoggedIn()):
		userDir = "accounts";
		components = command.split();
		if (len(components) < 4):
			self.connection.sendNotice(self.getRecipient(user,channel),"Usage: createaccount [username] [password] [confirm password]");
			self.connection.sendNotice(self.getRecipient(user,channel),"While your password will be stored securely, we do not make 100% guarantees, so proceed with caution. Use as safe and unique of a password as possible.");
		else:
			userFile = self.fileSystem.getFileContents(os.path.join(".",userDir,components[1].lower()+".txt"),0);
			if (userFile == None or len(userFile) <= 0):
				if (len(components[2]) < MIN_PASSWORD_LENGTH):
					self.connection.sendNotice(self.getRecipient(user,channel),"Your password is too short. Passwords must be at least "+str(MIN_PASSWORD_LENGTH)+" characters in length.");
				elif (components[2] != components[3]):
					self.connection.sendNotice(self.getRecipient(user,channel),"Your passwords do not match.");
				else:
					validUsername = 1;
					components[1] = components[1].replace("","");
					components[1] = components[1].replace("","");
					for i in range(0,16):
						for j in range(0,16):
							components[1] = components[1].replace(""+str(i)+","+str(j),"");
						components[1] = components[1].replace(""+str(i),"");
					components[1] = components[1].replace("","");
					components[1] = components[1].replace("","");
					if (len(components[1]) < MIN_USERNAME_LENGTH or len(components[1]) > MAX_USERNAME_LENGTH):
						self.connection.sendNotice(self.getRecipient(user,channel),"Your username must be between "+str(MIN_USERNAME_LENGTH)+" and "+str(MAX_USERNAME_LENGTH)+" characters long.");
						validUsername = 0;
					if (validUsername):
						for c in USERNAME_DISALLOWED_CHARS:
							if (components[1].find(c) >= 0):
								self.connection.sendNotice(self.getRecipient(user,channel),"Your username contains the character "+c+" -- it must not contain any of the following characters: "+USERNAME_DISALLOWED_CHARS);
								validUsername = 0;
								break;
						if (DISALLOWED_USERNAMES.count(components[1].lower())):
							self.connection.sendNotice(self.getRecipient(user,channel),"You are not permitted to use the name "+components[1]+". Please choose a different username.");
							validUsername = 0;
					if (validUsername):
						# CREATE THE ACCOUNT
						userFile = [];
						hashedPassword = hashlib.md5(components[2]).hexdigest();
						userFile.append(components[1]);
						userFile.append(hashedPassword);
						userFile.append(str(int(time()))); # registration time
						userFile.append("0"); # last login time
						userFile.append("0"); # total points
						userFile.append("0"); # available points
						userFile.append("1"); # user level
						userFile.append(""); # email address
						userFile.append(""); # real name
						userFile.append(""); # location
						userFile.append(""); # tagline
						userFile.append("n"); # gender
						userFile.append(user.nick+"!"+user.ident+"@"+user.host); # user identification stuff
						self.fileSystem.save(os.path.join(".",userDir,components[1].lower()+".txt"),userFile);
						self.connection.sendNotice(self.getRecipient(user,channel),"Thank you! Your account, with the username "+components[1]+", has been created.");
						self.connection.sendNotice(self.getRecipient(user,channel),"You may now login by using the command /msg "+self.connection.currentNick+" login "+components[1]+" [password]. Enjoy.");
			else:
				self.connection.sendNotice(self.getRecipient(user,channel),"The username "+components[1]+" seems to already be taken. Please pick a different username and try again.");
				
	else:
		self.connection.sendNotice(self.getRecipient(user,channel),"You are already logged in. Use the command logout to log out.");
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"This command may only be used over a private message. You wouldn't want people seeing our personal business, would you, "+user.nick+"?");
	self.connection.sendNotice(user.nick,"Type /msg "+self.connection.currentNick+" [command] to send a private message to me.");