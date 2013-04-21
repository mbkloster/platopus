# user misc script
# handles: accounthelp command, editing profile, requesting username changes, etc...

from Utility import wildcardHostname;
command = command.split(" ",1);

MAX_LOCATION_LEN = 45;
MAX_REALNAME_LEN = 30;
MAX_TAGLINE_LEN = 70;
MAX_EMAIL_LEN = 75;

def getRank(self, userFile):
	if (int(userFile[6]) <= 0):
		return "Banished Maggot";
	elif (int(userFile[6]) == 1):
		return "Lowly Plebe";
	elif (int(userFile[6]) == 2):
		return "Elder";
	else:
		return "God Incarnate for Life";

if (command[0].lower() == "whoami"):
	if (user.isLoggedIn()):
		self.callResponseScript("account_misc","whois $"+user.loginUsername,isDescription,user,channel,{});
	else:
		self.connection.sendMsg(self.getRecipient(user,channel),"You are not logged in and don't have a profile to view. To login, use /msg "+self.connection.currentNick+" login. To create an account, use /msg "+self.connection.currentNick+" createaccount.");
elif (command[0].lower() == "whois"):
	if (len(command) > 1):
		command[1] = command[1].split(" ",1)[0];
		matchType = 0; # any match type
		if (command[1][0:1] == "!"):
			command[1] = command[1][1:];
			matchType = 1; # nicks only
		elif (command[1][0:1] == "$"):
			command[1] = command[1][1:];
			matchType = 2; # users only
		if (command[1].lower() == "platopus" and user.nick.lower() != "platopus"):
			self.connection.sendMsg(self.getRecipient(user,channel),"I'm honestly slightly offended that you feel the need to waste my time with that question, "+user.getIdentity()+".");
		else:
			userMatch = None;
			nickMatch = None;
			if (command[1].lower() == "me" and user.isLoggedIn()):
				command[1] = user.loginUsername;
			for currentUser in self.connection.users:
				if (currentUser.nick.lower() == command[1].lower()):
					nickMatch = currentUser;
				if (currentUser.isLoggedIn() and currentUser.loginUsername.lower() == command[1].lower()):
					userMatch = currentUser;
				if (nickMatch != None and userMatch != None):
					break;
			userFile = None;
			if (userMatch != None and matchType != 1):
				userFile = self.fileSystem.getFileContents(os.path.join("accounts",userMatch.loginUsername.lower()+".txt"),0);
			elif (nickMatch != None and matchType != 2):
				userFile = self.fileSystem.getFileContents(os.path.join("accounts",nickMatch.loginUsername.lower()+".txt"),0);
			elif (matchType != 1):
				userFile = self.fileSystem.getFileContents(os.path.join("accounts",command[1].lower()+".txt"),0);
			
			if (userFile != None and len(userFile) >= 12):
				message = ""+userFile[0]+"";
				if (nickMatch != None and nickMatch.loginUsername.lower() == userFile[0].lower()):
					message += " ("+nickMatch.nick+")";
				elif (userMatch != None):
					message += " ("+userMatch.nick+")";
				if (userFile[8] != "" or userFile[9] != "" or userFile[10] != "" or userFile[11] != "n"):
					message += " is";
					if (userFile[11] == "m"):
						message += " a male";
					elif (userFile[11] == "f"):
						message += " a female";
					if (userFile[8] != ""):
						message += " named "+userFile[8]+"";
					if (userFile[9] != ""):
						message += " from "+userFile[9]+"";
					message += ".";
				else:
					message += " is a registered user.";
				if (userFile[11] == "m"):
					message += " He has";
				elif (userFile[11] == "f"):
					message += " She has";
				else:
					message += " They have";
				message += " "+userFile[5]+" available points ("+userFile[4]+" total).";
				if (userFile[11] == "m"):
					message += " His";
				elif (userFile[11] == "f"):
					message += " Her";
				else:
					message += " Their";
				message += " rank is "+getRank(self,userFile)+".";
				if (userFile[10] != ""):
					message += " Tagline: "+userFile[10];
				self.connection.sendMsg(self.getRecipient(user,channel),message);
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),"Sorry, I can't seem to find "+command[1]+" in the user database.");
	else:
		self.connection.sendMsg(self.getRecipient(user,channel),"You must specify a person to whois.");
elif (channel == ""):
	if (user.isLoggedIn()):
		if (command[0].lower() == "editprofile"):
			if (len(command) >= 2):
				parameters = command[1].split(" ",1);
			else:
				parameters = [];
			if (len(parameters) >= 1):
				if (len(parameters) < 2):
					parameters.append("");
				
				if (parameters[0] == "gender"): # GENDER
					parameters[1] = parameters[1].lower();
					if (parameters[1] == "m" or parameters[1] == "male" or parameters[1] == "mail" or parameters[1] == "masculine"):
						newGender = "m";
					elif (parameters[1] == "f" or parameters[1] == "female" or parameters[1] == "femail" or parameters[1] == "feminine"):
						newGender = "f";
					else:
						newGender = "n";
					genders = {"m":"Male","f":"Female","n":"Undisclosed"};
					user.gender = newGender;
					user.userFile[11] = newGender;
					user.saveUserFile();
					self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your gender has been changed to "+genders[newGender]+". Have fun!!!");
				elif (parameters[0] == "location"): # LOCATION
					if (len(parameters[1]) <= MAX_LOCATION_LEN):
						user.location = parameters[1].strip();
						user.userFile[9] = parameters[1].strip();
						user.saveUserFile();
						if (user.location != ""):
							self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your location has been set to "+parameters[1]+". Now go out and celebrate life.");
						else:
							self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your location has been unset. There's not much else left to say.");
					else:
						self.connection.sendNotice(self.getRecipient(user,channel),"Your location cannot be more than "+str(MAX_LOCATION_LEN)+" characters long.");
				elif (parameters[0] == "realname"): # REAL NAME!
					if (len(parameters[1]) <= MAX_REALNAME_LEN):
						user.realName = parameters[1].strip();
						user.userFile[8] = parameters[1].strip();
						user.saveUserFile();
						if (user.realName != ""):
							self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your real name has been set to "+parameters[1]+". By the way, I... well. I shouldn't say.");
						else:
							self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your real name has been unset. Well done team.");
					else:
						self.connection.sendNotice(self.getRecipient(user,channel),"Your real name cannot be more than "+str(MAX_REALNAME_LEN)+" characters long.");
				elif (parameters[0] == "tagline"): ### TAGLINE ###
					if (len(parameters[1]) <= MAX_TAGLINE_LEN):
						user.tagline = parameters[1].strip();
						user.userFile[10] = parameters[1].strip();
						user.saveUserFile();
						if (user.tagline != ""):
							self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your tagline has been set to "+parameters[1]+". Excellent choice.");
						else:
							self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your tagline has been unset. That was pretty funny!");
					else:
						self.connection.sendNotice(self.getRecipient(user,channel),"Your tagline cannot be more than "+str(MAX_TAGLINE_LEN)+" characters long.");
				elif (parameters[0] == "email"): # ****** EMAIL ******
					if (len(parameters[1]) <= MAX_EMAIL_LEN):
						parameters[1] = parameters[1].strip();
						if (parameters[1] == "" or (parameters[1].count(" ") <= 0 and parameters[1].count("@") == 1 and parameters[1].find("@") > 0 and parameters[1].find("@") < len(parameters[1])-1)):
							user.email = parameters[1];
							user.userFile[7] = parameters[1];
							user.saveUserFile();
							if (user.email != ""):
								self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your email has been changed to "+parameters[1]+". I can stop working now, right?");
							else:
								self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your email has been unset. I thought you liked getting my personal letters? We're through.");
						else:
							self.connection.sendNotice(self.getRecipient(user,channel),"This does not seem to be a valid email address. Please make sure it is typed correctly and try again.");
					else:
						self.connection.sendNotice(self.getRecipient(user,channel),"Your email cannot be more than "+str(MAX_EMAIL_LEN)+" characters long.");
			else:
				self.connection.sendNotice(self.getRecipient(user,channel),"Usage: editprofile [field] [new contents]");
				self.connection.sendNotice(self.getRecipient(user,channel),"Where [field] is the profile field you wish to change. It may be gender, location, realname,  tagline or email. Your 'tagline' is a short motto displayed in your profile.");
		elif (command[0].lower() == "accounthelp"):
			self.connection.sendNotice(self.getRecipient(user,channel),"To edit your profile, use editprofile [field] [new contents], where [field] may be gender, location, realname, tagline or email. Your 'tagline' is a short motto displayed in your profile.");
			self.connection.sendNotice(self.getRecipient(user,channel),"To log out, use logout. To manage computers that remember your account info, use managehosts. To change your password, use changepassword. To view your profile info, use the command whoami either in private message or in a channel.");
		elif (command[0].lower() == "managehosts"):
			if (len(command) <= 1):
				# just list hostnames
				wildcardHost = wildcardHostname(user.host).lower();
				userhosts = self.fileSystem.getFileContents(os.path.join("misc","userhosts.txt"),0);
				relevantHosts = [];
				for host in userhosts:
					host = host.split(" ");
					if (len(host) >= 2 and host[0] != wildcardHost and host[1].lower() == user.loginUsername.lower()):
						relevantHosts.append(host[0]);
				if (len(relevantHosts) >= 1):
					message = "The following other hostnames are associated with this account:";
					for relevantHost in relevantHosts:
						message += " "+relevantHost;
					self.connection.sendNotice(self.getRecipient(user,channel),message);
					self.connection.sendNotice(self.getRecipient(user,channel),"To remove one or more hostnames from rememberance, simply use the command managehosts [host(s) to remove]. To stop being remembered on this computer, simply log out with logout.");
				else:
					self.connection.sendNotice(self.getRecipient(user,channel),"You do not have this account remembered on any other computers. To stop me from remembering you on this computer, use the command logout.");
			else:
				# actually try and remove hostnames
				userhosts = self.fileSystem.getFileContents(os.path.join("misc","userhosts.txt"),0);
				wildcardHost = wildcardHostname(user.host).lower();
				hosts = command[1].split(" ");
				hostsRemoved = 0;
				for host in hosts:
					host = host.lower();
					if (host != wildcardHost and userhosts.count(host+" "+user.loginUsername)):
						userhosts.remove(host+" "+user.loginUsername);
						hostsRemoved += 1;
				if (hostsRemoved == 1):
					self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Removed one host from remembering your account.");
					self.fileSystem.save(os.path.join("misc","userhosts.txt"),userhosts);
				elif (hostsRemoved > 0):
					self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Removed "+str(hostsRemoved)+" hosts from remembering your account.");
					self.fileSystem.save(os.path.join("misc","userhosts.txt"),userhosts);
				else:
					self.connection.sendNotice(self.getRecipient(user,channel),"Sorry, but I couldn't seem to find any of the hosts you specified to remove.");
		elif (command[0].lower() == "changepassword"):
			if (len(command) > 1):
				parameters = command[1].split();
			else:
				parameters = [];
			if (len(parameters) < 3):
				self.connection.sendNotice(self.getRecipient(user,channel),"Usage: changepassword [current password] [new password] [confirm new password]");
			else:
				hashedOldPassword = hashlib.md5(parameters[0]).hexdigest();
				userFile = self.fileSystem.getFileContents(os.path.join("accounts",user.loginUsername.lower()+".txt"));
				if (userFile != None and len(userFile) >= 2):
					if (hashedOldPassword == userFile[1]):
						if (parameters[1] == parameters[2]):
							MIN_PASSWORD_LENGTH = 6;
							if (len(parameters[1]) >= MIN_PASSWORD_LENGTH):
								userFile[1] = hashlib.md5(parameters[1]).hexdigest();
								self.fileSystem.save(os.path.join("accounts",user.loginUsername.lower()+".txt"),userFile);
								self.connection.sendNotice(self.getRecipient(user,channel),"Thank you. Your password has been successfully changed.");
							else:
								self.connection.sendNotice(self.getRecipient(user,channel),"Your password must be at least "+str(MIN_PASSWORD_LENGTH)+" characters long.");
						else:
							self.connection.sendNotice(self.getRecipient(user,channel),"Your password and confirm password do not match. Make sure they do, and try again. Remember, both passwords are case sensitive!");
					else:
						self.connection.sendNotice(self.getRecipient(user,channel),"Your current password is not correctly specified. Please make sure it is correct and try again. Remember, it is case sensitive!");
				else:
					self.connection.sendNotice(self.getRecipient(user,channel),"There was a file error on my end while trying to change your password. Relax, this was nothing to do with you. Please try again momentarily, and if it persists, contact iCeD.");
						
	else:
		self.connection.sendNotice(self.getRecipient(user,channel),"You must be logged in to use this command.");
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"This command may only be used over a private message. You wouldn't want people seeing our personal business, would you, "+user.nick+"?");
	self.connection.sendNotice(user.nick,"Type /msg "+self.connection.currentNick+" [command] to send a private message to me.");