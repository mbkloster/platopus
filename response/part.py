# part script
# handles parts from users in this format: [nick] [channel] [part message]
if ((user == None or user.nick.lower() == self.connection.currentNick.lower()) and self.channelEncoreHistory.has_key(channel.lower())):
	del self.channelEncoreHistory[channel.lower()];