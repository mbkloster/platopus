# kick script

command = command.split(" ",4);

if (channel != "" and self.isOpInChannel(user.nick,channel)):
	if (len(command) >= 3):
		nick = command[1];
		if (nick.lower() == self.connection.currentNick.lower()):
			nick = user.nick;
		try:
			if (command[2][-1:] == "%"):
				chance = float(command[2][0:-1])/100;
			else:
				chance = 1/float(command[2]);
			if (chance > 0.5 or chance <= 0):
				self.connection.sendMsg(self.getRecipient(user,channel),"Chance must be between 0% and 50% (1 in 2).");
			elif (self.isInChannel(nick,channel)):
				self.console.setVar("rankick_target",nick);
				self.console.setVar("rankick_chance",chance);
				self.console.setVar("rankick_channel",channel);
				self.connection.sendMsg(self.getRecipient(user,channel),"Random Kicker on "+nick+" -- Chance: 1 in "+str(int(1/chance))+" ("+str(chance*100)+"%)");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),"I can't seem to find "+nick+" in "+channel+".");
					
		except ValueError:
			self.connection.sendMsg(self.getRecipient(user,channel),"You must enter a valid number or percentage for the random kick chance.");
	elif (len(command) == 2 and command[1].lower() == "off"):
		self.console.setVar("rankick_target","");
		self.console.setVar("rankick_chance",0);
		self.console.setVar("rankick_channel","");
		self.connection.sendMsg(self.getRecipient(user,channel),"Random Kicker has been disabled.");
	else:
		self.connection.sendMsg(self.getRecipient(user,channel),"Usage: rankick [nick] [chance]");
					
elif (channel == ""):
	self.connection.sendMsg(self.getRecipient(user,channel),"This command must be used on a channel.");
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"Only ops may use this command.");