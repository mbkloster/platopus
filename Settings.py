########################################
# platopus settings
########################################
#
# A one-stop shop for all yo platopus settings.
#

class Settings:
	# Server(s) to connect to.
	IRC_SERVER = "us.quakenet.org";
	# Port to use.
	IRC_PORT = 6667;
	
	# Desired nicks, in order
	NICKS = ["platopus2","pusoplat","platoplatopus","playdoughpus"];
	
	# Login username.
	LOGIN_USER = "grapefruit";
	# Login domain.
	LOGIN_DOMAIN = "coleslaw.com";
	# Login real name.
	LOGIN_REAL_NAME = "part philosopher, part semi-aquatic mammal";
	
	# Auto-join channels
	AUTO_JOIN_CHANNELS = ["#platopus",];
	# Channels that use exclamation notation (eg: !command)
	SHORT_NOTATION_CHANNELS = ["#platopus",];
	
	# Default quit message.
	QUIT_MESSAGE = "duck duck duck duck duck duck duck duck duck ELEPHANT";
	
	# Auto-connect to server on startup?
	AUTO_CONNECT = 1;
	# Auto-reconnect upon disconnection?
	AUTO_RECONNECT = 1;
	# Auto-reconnect delay (in seconds)
	AUTO_RECONNECT_DELAY = 45;
	# Max auto-reconnect attempts
	MAX_AUTO_RECONNECT_ATTEMPTS = 9999;
	
	# Auto-rejoin channel on kick?
	AUTO_REJOIN = 1;
	# Auto-rejoin delay (in seconds)
	AUTO_REJOIN_DELAY = 5.0;
	# Max auto-rejoin attempts
	AUTO_REJOIN_MAX_ATTEMPTS = 60;
	
	# Lines to send to the server on connection. In order.
	CONNECT_PERFORM_LINES = ["PRIVMSG Q@CServe.QuakeNet.org :AUTH platopus a","MODE {currentnick} +x"];
