# nick change script
# Command is in this format: oldnick newnick
command = command.split(" ");

if (self.console.getVar("rankick_target") != "" and self.console.getVar("rankick_chance") > 0 and self.console.getVar("rankick_channel") != ""):
	if (command[0].lower() == self.console.getVar("rankick_target").lower()):
		self.console.setVar("rankick_target",command[1]);
		self.connection.sendMsg(self.console.getVar("rankick_channel"),"Nice try, "+command[0]+". Random Kicker is now on "+command[1]+".");