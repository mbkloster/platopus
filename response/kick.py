# kick script

command = command.split(" ",2);

if (channel != "" and self.isOpInChannel(user.nick,channel)):
	if (len(command) >= 3):
		nick = command[1];
		if (nick.lower() == self.connection.currentNick.lower()):
			nick = user.nick;
		reason = command[2];
		if (self.isInChannel(nick,channel)):
			self.connection.kickUser(channel,nick,reason);
		else:
			self.connection.sendMsg(self.getRecipient(user,channel),"I can't seem to find "+nick+" in "+channel+".");
	else:
		self.connection.sendMsg(self.getRecipient(user,channel),"Usage: kick [nick] [reason]");
					
elif (channel == ""):
	self.connection.sendMsg(self.getRecipient(user,channel),"This command must be used on a channel.");
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"Only ops may use this command.");