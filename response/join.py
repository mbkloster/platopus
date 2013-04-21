# Join channel response script
# handles joins from users in this format: [nick] [channel]

from Utility import wildcardHostname;
if (channel[0:1] != "#"):
	channel = "#"+channel;

WELCOME_MESSAGES = {
"#platopus":"Welcome to #platopus, {theirnick}! This place is for all your platopus testing and screwing around needs. Remember: Commands here don't need to be prefixed with \"platopus \", only an exclamation mark (!). Command list at: http://platopus.senselesspoliticalramblings.com/commands.html."
};

user.checkHostnameRememberance(self.fileSystem, self.console);
if (WELCOME_MESSAGES.has_key(channel.lower())):
	message = WELCOME_MESSAGES[channel.lower()];
	message = message.replace("{theirnick}",user.nick);
	if (user.isLoggedIn()):
		message += " You have been logged in as "+user.loginUsername+". For a list of user commands, message me with accounthelp.";
	self.connection.sendNotice(user.nick,message);