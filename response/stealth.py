# stealth script
# execute commands in another channel without their consent. spooooooky
from threading import Thread;

command = command.split(" ",2);
if (len(command) >= 3):
	targetChannel = command[1];
	command = command[2];
	if (targetChannel.lower() == channel.lower()):
		self.connection.sendMsg(self.getRecipient(user,channel),"Are you fucking kidding me? This is "+targetChannel+". Jesus Christ, you're an idiot.");
	elif (targetChannel[0:1] != "#"):
		self.connection.sendMsg(self.getRecipient(user,channel),"You must specify a channel to use this stealth command in. Remember: I don't do stealth commands to users.");
	elif (not self.connection.channels.has_key(targetChannel.lower())):
		self.connection.sendMsg(self.getRecipient(user,channel),"I'm not even in "+targetChannel+". Are you trying to waste my time or are you just that obtuse?");
	elif (user.loginUserLevel >= 2 or self.checkPointRequirement(user,channel,150,"execute a stealth command")):
		self.console.threads["stealth"] = Thread(target=self.callResponse,args=(command,0,user,targetChannel,0));
		self.console.threads["stealth"].start();
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"Usage: stealth [channel] [command]");