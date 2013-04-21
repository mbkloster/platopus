# SHUT UP script

from threading import Timer;

SHUP_POINT_COST = 150;

def unshup(self, channel, duration, shuppingUser, targetUser):
	self.connection.sendMsg(channel,""+targetUser.nick+"'s "+toFormattedTime(duration)+" of shup time from "+shuppingUser.nick+" have ended.");
	self.connection.setMode(channel+" -b *!*@"+targetUser.host);

command = command.split(" ",3);

if (channel != "" and user.channels.has_key(channel.lower()) and (user.channels[channel.lower()] or (user.isLoggedIn() and user.availablePoints >= SHUP_POINT_COST) or user.loginUserLevel >= 3)):
	if (not parameters.has_key("unshup")):
		if (len(command) >= 3):
			nick = command[1];
			duration = fromFormattedTime(command[2]);
			if (len(command) >= 4):
				reason = command[3];
			else:
				reason = self.fileSystem.getRandomLine(os.path.join("misc","shupreasons.txt"));
			userFound = self.connection.getUser(nick);
			if (self.isInChannel(nick,channel) and not self.isOpInChannel(nick,channel)):
				if (duration >= 10):
					if (user.channels[channel.lower()] or user.loginUserLevel >= 3 or duration < 900):
						if (not user.channels[channel.lower()] and user.loginUserLevel < 3):
							user.deductPoints(SHUP_POINT_COST);
						self.connection.sendMsg(self.getRecipient(user,channel),""+userFound.nick+" has received "+toFormattedTime(duration)+" of shut up time from "+user.nick+" (Reason: "+reason+")");
						self.connection.setMode(channel+" +b *!*@"+userFound.host);
						if (self.console.hasThread("shup_"+userFound.host) and self.console.threads["shup_"+userFound.host].isAlive()):
							self.console.threads["shup_"+userFound.host].cancel();
						self.console.threads["shup_"+userFound.host] = Timer(duration,unshup,args=(self,channel,duration,user,userFound));
						self.console.threads["shup_"+userFound.host].start();
					elif (not user.channels[channel.lower()] and user.loginUserLevel < 3):
						self.connection.sendMsg(self.getRecipient(user,channel),"If you are not an op, you may not give a shup time lasting longer than 15 minutes.");
				else:
					self.connection.sendMsg(self.getRecipient(user,channel),"Shup time duration must be at least 10 seconds long.");
			elif (self.isOpInChannel(nick,channel)):
				self.connection.sendMsg(self.getRecipient(user,channel),""+nick+" seems to be a "+channel+" op, and my religious principles forbid me from using shup time on ops.");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),"I can't seem to find "+nick+" in "+channel+".");
		else:
			self.connection.sendMsg(self.getRecipient(user,channel),"Usage: shup [nick] [duration] [reason (optional)]");
	else:
		if (len(command) >= 2):
			nick = command[1];
			userFound = self.connection.getUser(nick);
			if (userFound != None and userFound.channels.has_key(channel.lower())):
				if (self.console.hasThread("shup_"+userFound.host) and self.console.threads["shup_"+userFound.host].isAlive()):
					self.console.threads["shup_"+userFound.host].cancel();
					self.connection.sendMsg(channel,""+userFound.nick+" has been given a shup time pardon from "+user.nick+".");
					self.connection.setMode(channel+" -b *!*@"+userFound.host);
				else:
					self.connection.sendMsg(channel,"Does "+userFound.nick+" even have a shup time active? You're wasting my time, you dick.");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),"I can't seem to find "+nick+" in "+channel+".");
					
elif (channel == ""):
	self.connection.sendMsg(self.getRecipient(user,channel),"This command must be used on a channel.");
else:
	if (user.isLoggedIn()):
		self.connection.sendMsg(self.getRecipient(user,channel),"To use this command, you must either be an op or have "+str(SHUP_POINT_COST)+" available points.");
	else:
		self.connection.sendMsg(self.getRecipient(user,channel),"To use this command, you must either be an op or be logged in and have "+str(SHUP_POINT_COST)+" available points.");
		self.connection.sendMsg(self.getRecipient(user,channel),"To login, use /msg "+self.connection.currentNick+" login. To create an account, use /msg "+self.connection.currentNick+" createaccount.");