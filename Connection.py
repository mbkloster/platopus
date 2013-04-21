########################################
# platopus connection class
########################################
#
# This holds all the socket/irc protocol information for platopus,
# including some basic functions for doing things like joining
# channels, sending messages, etc.

from socket import *;
from threading import *;
from time import sleep, time;
from Utility import getSuffixFromList, wildcardHostname;
from Settings import Settings;
import sys; # system functions
import os;
import random;

class User:
	
	# How long until a private conversation becomes irrelevant (in s)?
	PRIVATE_CONVERSATION_TIMEOUT = 600;
	
	""" Defines a single instance of a user on a channel. """
	def __init__(self, nick, ident = "", host = ""):
		self.nick = nick;
		self.ident = ident;
		self.host = host;
		self.channels = {}; # a list of channels, and whether or not they have ops/voice in said channel
		self.lastPrivateMsg = 0; # Timestamp of the last private message received.
		self.lastPublicMsg = 0; # Timestamp of the last public message received.
		
		self.loginUsername = "";
		self.loginUserLevel = 0;
		self.totalPoints = 0;
		self.availablePoints = 0;
		self.tagline = "";
		self.realName = "";
		self.gender = "n";
		self.userFile = None;
		self.fileSystem = None;
		
		self.hostLookupPending = 0;
		
		self.encoreHistory = [];
	
	def joinChannel(self, channel):
		if (not self.channels.has_key(channel)):
			self.channels[channel] = 0;
	
	def partChannel(self, channel):
		if (self.channels.has_key(channel)):
			del self.channels[channel];
	
	def opOnChannel(self, channel):
		if (self.channels.has_key(channel)):
			self.channels[channel] = 1;
	
	def deopOnChannel(self, channel):
		if (self.channels.has_key(channel)):
			self.channels[channel] = 0;
	
	def updateLastPrivateMsg(self):
		self.lastPrivateMsg = time();
		
	def updateLastPublicMsg(self):
		self.lastPublicMsg = time();
		
	def isStillRelevant(self):
		""" Checks if the user is still 'relevant' - either on a channel or recently talked to the bot """
		if (len(self.channels) > 0 or time()-self.lastPrivateMsg < self.PRIVATE_CONVERSATION_TIMEOUT):
			return 1;
		else:
			return 0;
	
	def getIdentity(self):
		""" Gets an identifier (right now, just the nick) for this user) """
		return self.nick;
	
	def isLoggedIn(self):
		""" Checks if the user is logged in and gives a boolean true/false result. """
		return (self.loginUsername != "" and self.loginUserLevel > 0);
	
	def attemptLogin(self, username, password, fileSystem, isTemporary = 0):
		""" Attempts to login with a specified username and password (password must be pre-hashed) and returns (true/false, error msg) depending on the success of the login """
		userDir = "accounts";
		userFileContents = fileSystem.getFileContents(os.path.join(".",userDir,username.lower()+".txt"),0);
		if (not self.isLoggedIn()):
			if (userFileContents == None or len(userFileContents) <= 0):
				#print os.path.join(".",userDir,usermame.lower()+".txt");
				return (0,"Invalid username and/or password. Make sure both were typed correctly and try again.");
			else:
				#print password+" "+userFileContents[1];
				if (password == userFileContents[1]):
					self.loginUsername = userFileContents[0];
					try:
						self.loginUserLevel = int(userFileContents[6]);
					except ValueError:
						self.loginUserLevel = 1;
					try:
						self.totalPoints = int(userFileContents[4]);
					except ValueError:
						self.totalPoints = 0;
					try:
						self.availablePoints = int(userFileContents[5]);
					except ValueError:
						self.avaialblePoints = 0;
					self.realName = userFileContents[6];
					self.location = userFileContents[7];
					self.tagline = userFileContents[8];
					userFileContents[3] = str(int(time()));
					fileSystem.save(os.path.join(".",userDir,username.lower()+".txt"),userFileContents);
					self.userFile = userFileContents;
					self.fileSystem = fileSystem;
					return (1,"");
				else:
					return (0,"Invalid username and/or password. Make sure both were typed correctly and try again.");
		else:
			return (0,"You are already logged in.");
	
	def checkHostnameRememberance(self, fileSystem, console):
		if (not self.isLoggedIn()):
			# try and auto-login this user
			userhosts = fileSystem.getFileContents(os.path.join("misc","userhosts.txt"),0);
			wildcardHost = wildcardHostname(self.host).lower();
			
			for entry in userhosts:
				entry = entry.split(" ");
				if (len(entry) >= 2):
					if (entry[0] == wildcardHost):
						# found a hostname match!
						username = entry[1];
						userFile = fileSystem.getFileContents(os.path.join("accounts",username.lower()+".txt"),0);
						if (userFile != None and len(userFile) >= 2):
							username = userFile[0];
							password = userFile[1];
							loginAttempt = self.attemptLogin(username,password,fileSystem);
							if (loginAttempt[0]):
								console.output("Automatically logged "+self.nick+" in as "+self.loginUsername+".");
							else:
								console.output("Could not automatically log "+self.nick+" in. An error occured.");
	
	def logout(self):
		""" Logs out. Returns (true/false, error msg) depending on the results of the logout. """
		if (self.isLoggedIn()):
			self.loginUsername = "";
			self.loginUserLevel = 0;
			return (1,"");
		else:
			return (0,"You are not logged in.");
	
	def saveUserFile(self):
		userDir = "accounts";
		self.fileSystem.save(os.path.join(".",userDir,self.loginUsername.lower()+".txt"),self.userFile);
	
	def addPoints(self, points):
		if (self.isLoggedIn()):
			self.totalPoints += points;
			self.availablePoints += points;
			self.userFile[4] = str(self.totalPoints);
			self.userFile[5] = str(self.availablePoints);
			self.saveUserFile();
	
	def deductPoints(self, points):
		if (self.isLoggedIn()):
			self.availablePoints -= points;
			if (self.availablePoints < 0):
				self.availablePoints = 0;
			self.userFile[5] = str(self.availablePoints);
			self.saveUserFile();
	
	def getRank(self):
		if (self.loginUserLevel <= 0):
			return "Banished Maggot";
		elif (self.loginUserLevel == 1):
			return "Lowly Plebe";
		elif (self.loginUserLevel == 2):
			return "Elder";
		else:
			return "God Incarnate for Life";
	
	def addToEncoreHistory(self, command):
		MAX_HISTORY_LEN = 5;
		self.encoreHistory.append(command);
		if (len(self.encoreHistory) > MAX_HISTORY_LEN):
			self.encoreHistory = self.encoreHistory[1:];
	
	def removeFromEncoreHistory(self):
		self.encoreHistory = self.encoreHistory[0:len(encoreHistory)-1];
	
class Connection (socket):
	
	# irc port of choice
	IRC_PORT = 6666;
	
	# join delay between channels (in seconds)
	JOIN_DELAY = 1.0;
	
	# timeout delay (in seconds)
	TIMEOUT = 300;
	
	# ping delay (in seconds - should be lower than the above value - servers are usually at 180)
	PING_DELAY = 195;
	# max manual pings before declaring a connection error...
	MAX_PINGS = 3;
	
	# names the bot will respond to... aside from the current nick, obviously
	RESPONSE_NAMES = ["platopus",];
	
	IRRELEVANT_USER_CHECK_TIME = 60;
	
	# Self-check message flood limit (in form (message,time period))
	MESSAGE_FLOOD_LIMIT = (3,4);
	
	# Max message length (before it splits the message up into small bits)
	MAX_MESSAGE_LEN = 415;
	
	# Max messages sent from one request
	MAX_MESSAGES_PER_REQUEST = 2;
	
	# Channel modes that take parameters.
	PARAMETER_MODES = "bklov";
	
	def __init__(self, nicks, loginUser, loginDomain, loginRealName, server, port = IRC_PORT):
		""" Initializes an irc connection. """
		socket.__init__(self,AF_INET,SOCK_STREAM,IPPROTO_TCP);
		
		self.nicks = nicks;
		self.currentNick = "";
		self.currentServer = "";
		
		self.loginUser = loginUser;
		self.loginDomain = loginDomain;
		self.loginRealName = loginRealName;
		self.server = server;
		self.port = port;
		
		self.activelySending = 0;
		self.connected = 0;
		self.connecting = 0;
		
		self.channels = {}; # currently joined channels, and a user list for those channels
		self.channelRejoins = {}; # a tally of rejoin attempts for each channel
		self.autoJoinChannels = []; # channels we hope to join
		self.users = []; # unsorted list of users
		
		self.quitMessage = "";
		
		self.console = None;
		self.responseSystem = None;
		
		self.settimeout(self.TIMEOUT);
		
		self.needsRefresh = 0; # when we disconnect or get timed out, this socket will need to be refreshed (replaced)
		self.pings = 0; # number of manual timeout pings done.. kill this connection after this exceeds a certain amount
		
		self.messageTimes = [];
	
	def consoleOutput(self, text):
		""" Checks to see that the console object exists and if so, outputs a line to it """
		if (self.console != None):
			self.console.output(text);
	
	def connectionError(self):
		if (self.connected or self.connecting):
			errno, errstr = sys.exc_info()[:2];
			if (errstr != None):
				self.consoleOutput("! "+str(errstr[0])+" "+str(errstr[1]));
			else:
				self.consoleOutput("! Connection error");
			self.connected = 0;
			self.connecting = 0;
			if (Settings.AUTO_RECONNECT):
				self.console.reconnect();
		
	
	def removeUser(self, nick):
		""" Derefences a user completely. Use when they quit out. """
		nick = nick.lower();
		if (nick != self.currentNick.lower()):
			for channel, channelUsers in self.channels.items():
				for user in channelUsers:
					if (user.nick.lower() == nick):
						self.channels[channel.lower()].remove(user);
			
			for user in self.users:
				if (user.nick.lower() == nick):
					for channel, status in user.channels.items():
						if (self.channels[channel.lower()].count(user) > 0):
							self.channels[channel.lower()].remove(user);
					self.users.remove(user);
	def incrementChannelRejoins(self, channel):
		""" Increments the max number of channel rejoins. Returns whether or not more rejoins will be permissable. """
		if (self.channelRejoins.has_key(channel)):
			self.channelRejoins[channel] += 1;
		else:
			self.channelRejoins[channel] = 1;
		return self.channelRejoins[channel] <= Settings.AUTO_REJOIN_MAX_ATTEMPTS;
	
	def setAutoRejoinTimer(self, channel):
		""" Sets up the auto-rejoin timer """
		self.console.threads["rejoin_"+channel.lower()] = Timer(Settings.AUTO_REJOIN_DELAY,self.joinChannel,(channel,1,));
		self.console.threads["rejoin_"+channel.lower()].setDaemon(1);
		self.console.threads["rejoin_"+channel.lower()].start();
	
	def removeIrrelevantUsers(self):
		""" Removes users no longer considered 'relevant' (in no channel and not having spoken to the bot in a while) """
		sleep(self.IRRELEVANT_USER_CHECK_TIME);
		while (self.connected):
			for user in self.users:
				if (not user.isStillRelevant()):
					self.removeUser(user.nick);
			sleep(self.IRRELEVANT_USER_CHECK_TIME);
	
	def joinUserToChannel(self, user, channel):
		channel = channel.lower();
		if (not user.channels.has_key(channel)): # make sure they're not already on the channel
			if (self.users.count(user) < 1):
				self.users.append(user);
			if (not self.channels.has_key(channel)):
				self.channels[channel] = [];
			self.channels[channel].append(user);
			user.joinChannel(channel);
	
	def partUserFromChannel(self, user, channel):
		channel = channel.lower();
		self.channels[channel].remove(user);
		user.partChannel(channel);
		if (not user.isStillRelevant()):
			self.removeUser(user.nick);
	
	def IRCConnect(self):
		""" Connects to the irc server. """
		self.connecting = 1;
		self.consoleOutput("Connecting to server "+self.server+" (port "+str(self.port)+")...");
		try:
			self.connect((self.server, self.port));
			line = "";
			while (line.strip() == ""):
				line = self.getNetLine();
			if (line.lower().find("notice auth") == -1):
				self.consoleOutput("Server "+self.server+":"+str(self.port)+" does not seem to be a valid IRC server.");
				self.connected = 0;
				self.connecting = 0;
				self.close();
				if (Settings.AUTO_RECONNECT):
					self.console.reconnect();
				return 0;
			else:
				self.consoleOutput("Connected. Logging on...");
				self.sendLine("USER "+self.loginUser+" "+self.loginUser+" "+self.loginDomain+" :"+self.loginRealName);
				self.sendLine("NICK "+self.nicks[0]);
				self.currentNick = self.nicks[0];
				nicksUsed = 1;
				line = self.getNetLine();
				while (line.find(" 001 ") <= -1):
					if (line.find(" 433 ") >= 0 or line.find(" 432 ") >= 0):
						# nick already in use, so try the next nickname...
						if (nicksUsed >= len(self.nicks)):
							self.consoleOutput("All nicknames already in use. Cancelling connection.");
							self.sendLine("QUIT");
							self.connected = 0;
							self.connecting = 0;
							self.close();
							if (Settings.AUTO_RECONNECT):
								self.console.reconnect();
							return 0;
						else:
							self.sendLine("NICK "+self.nicks[nicksUsed]);
							self.currentNick = self.nicks[nicksUsed];
							nicksUsed += 1;
					elif (line[0:6].lower() == "ping :"):
						self.sendLine("PONG "+line[5:]);
					line = self.getNetLine();
				
				server = line.split()[0];
				self.currentServer = server[1:];
				self.consoleOutput("Logged on to "+self.currentServer+" as "+self.currentNick);
				self.connected = 1;
				self.connecting = 0;
				
				for performLine in Settings.CONNECT_PERFORM_LINES:
					performLine = performLine.replace("{currentnick}",self.currentNick);
					self.sendLine(performLine);
				
				if (self.console != None):
					self.console.threads["listen"] = Thread(target=self.listen);
					self.console.threads["listen"].start();
					
					self.console.threads["remove_irrelevant_users"] = Thread(target=self.removeIrrelevantUsers);
					self.console.threads["remove_irrelevant_users"].setDaemon(1);
					self.console.threads["remove_irrelevant_users"].start();
					
					# add in timers for auto-join timers
					joinTimerList = [];
					joinDelay = 0.0;
					for channel in self.autoJoinChannels:
						joinDelay += self.JOIN_DELAY;
						newTimer = Timer(joinDelay,self.joinChannel,(channel,));
						newTimer.start();
						joinTimerList.append(newTimer);
					self.console.threads["auto_join"] = joinTimerList;
				return 1;
		except error:
			self.connectionError();
	
	def getUser(self, nick):
		""" Gets a user by nick reference. If no such user exists, return None. """
		nick = nick.lower();
		for user in self.users:
			if (user.nick.lower() == nick):
				return user;
		return None;
	
	def getUserFromUsername(self, username):
		""" Gets a user by a username reference. If no such user exists, return None. """
		username = username.lower();
		for user in self.users:
			if (user.loginUsername.lower() == username):
				return user;
		return None;
	
	def getUserAdvanced(self, username):
		""" Combines the functionality of the above functions. """
		searchMode = 0; # search both nicks and users
		if (username[0:1] == "!"):
			searchMode = 1; # nicks only
		elif (username[0:1] == "$"):
			searchMode = 2; # users only
		
		if (username[0:1] == "!" or username[0:1] == "$"):
			username = username[1:];
		
		nickMatch = self.getUser(username);
		if (searchMode == 1):
			return nickMatch;
		
		userMatch = self.getUserFromUsername(username);
		if (searchMode == 2):
			return userMatch;
		if (nickMatch != None and userMatch != None):
			if (userMatch.loginUserLevel >= nickMatch.loginUserLevel):
				return userMatch;
			else:
				return nickMatch;
		elif (nickMatch != None):
			return nickMatch;
		else:
			return userMatch;
	
	def getNetLine(self):
		""" Receives a line from the connection. """
		line = "";
		while (self.connected or self.connecting):
			try:
				c = self.recv(1);
			except error:
				# encountered a read error while trying to get a char... probably a premature disconnection
				# remember: bad file descriptor is #9
				self.connectionError();
				return "";
			if (c != "\n" and c != "\r"):
				line += c;
			else:
				break;
		#print "got: "+line;
		return line;
	
	def sendLine(self, line):
		""" Sends a line of irc code. """
		while (self.activelySending or not (self.connected or self.connecting)):
			""" don't send anything else if we're currently sending stuff over the connection """
			sleep(0.0002);
		#print "sending: "+line;
		if (self.connected or self.connecting):
			self.activelySending = 1;
			try:
				for c in line:
					self.send(c);
				self.send("\n\r");
				if (self.connected):
					# run our ping thread
					if (self.console.threads.has_key("ping")):
						self.console.threads["ping"].cancel();
					self.console.threads["ping"] = Timer(self.PING_DELAY,self.ping);
					self.console.threads["ping"].setDaemon(1);
					self.console.threads["ping"].start();
			except error, timeout:
				self.connectionError();
			finally:
				self.activelySending = 0;
			return 1;
		else:
			# not connected... so return false;
			self.activelySending = 0;
			return 0;
			
	def ping(self):
		# PING! Usually used to check for a timeout.
		self.pings += 1;
		if (self.pings <= self.MAX_PINGS):
			self.consoleOutput("Performing timeout ping...");
			self.sendLine("PING :"+str(int(time())));
			self.consoleOutput("Timeout ping done.");
		else:
			self.connectionError();
	
	def listen(self):
		""" Passively receives and handles lines. Should be called after connected to the IRC server. """
		while (self.connected):
			line = self.getNetLine();
			self.pings = 0;
			if (line[0:6].lower() == "ping :"):
				self.sendLine("PONG "+line[5:]);
			if(line[0:1] == ":" and line.find(" ") >= 0):
				line = line.split(" ",1);
				hostname = line[0];
				hostname = hostname[1:];
				line = line[1];
				lowerLine = line.lower();
				
				user = None;
				if (hostname.find("!") >= 0 and hostname.find("@") >= 0 and hostname.find("@") > hostname.find("!")):
					nick = hostname[0:hostname.find("!")];
					ident = hostname[hostname.find("!")+1:hostname.find("@")];
					hostname = hostname[hostname.find("@")+1:];
					user = self.getUser(nick);
					if (user == None):
						# create new user
						user = User(nick, ident, hostname);
						self.users.append(user);
					else:
						# update ident/hostname for an existing user
						user.ident = ident;
						user.hostname = hostname;
				else:
					# server action
					nick = hostname;
					ident = "";
					
				prefixes = ["join","part","quit","privmsg","notice","nick","kick","mode","302","353","404","471","472","473","474","475"];
				prefixSuffix = getSuffixFromList(line,lowerLine,prefixes);
				if (prefixSuffix != None):
					if (prefixSuffix[0] == "join"):
						# Someone (either us or someone else) is joining the channel
						if (user != None):
							user.updateLastPublicMsg();
						if (nick.lower() == self.currentNick.lower()):
							self.channels[prefixSuffix[1].lower()] = [];
							self.consoleOutput("Joined channel "+prefixSuffix[1]+".");
							if (not self.responseSystem.channelEncoreHistory.has_key(prefixSuffix[1].lower())):
								# add the channel encore list
								self.responseSystem.channelEncoreHistory[prefixSuffix[1].lower()] = [];
							
							if (self.channelRejoins.has_key(prefixSuffix[1].lower())):
								del self.channelRejoins[prefixSuffix[1].lower()];
						else:
							self.consoleOutput(prefixSuffix[1]+" JOIN "+nick);
							if (user != None):
								self.joinUserToChannel(user,prefixSuffix[1]);
							# now report it to our response script
							self.console.threads["join"] = Thread(target=self.responseSystem.callResponseScript,args=("join",user.nick+" "+prefixSuffix[1],0,user,prefixSuffix[1]));
							self.console.threads["join"].start();
						
					elif (prefixSuffix[0] == "part"):
						# Someone (either us or someone else) is parting the channel
						if (prefixSuffix[1].find(" ") < 0):
							channel = prefixSuffix[1];
							message = "";
						else:
							channel = prefixSuffix[1].split(" ",1)[0];
							message = prefixSuffix[1].split(" ",1)[1][1:];
						if (user != None):
							self.partUserFromChannel(user,channel);
						if (nick.lower() == self.currentNick.lower()):
							del self.channels[channel.lower()];
							if (message == ""):
								self.consoleOutput("Parted channel "+channel+".");
							else:
								self.consoleOutput("Parted channel "+channel+" ("+message+").");
						else:
							if (message == ""):
								self.consoleOutput(channel+" PART "+nick);
							else:
								self.consoleOutput(channel+" PART "+nick+" ("+message+")");
							# now report it to our response script
							self.console.threads["part"] = Thread(target=self.responseSystem.callResponseScript,args=("part",user.nick+" "+channel+" "+message,0,user,channel));
							self.console.threads["part"].start();
							
							if (user != None and not user.isStillRelevant()):
								self.removeUser(user.nick);
					elif (prefixSuffix[0] == "quit"):
						if (nick.lower() != self.currentNick.lower()):
							self.consoleOutput(nick+" QUIT ("+prefixSuffix[1][1:]+")");
							# now report it to our response script
							self.console.threads["quit"] = Thread(target=self.responseSystem.callResponseScript,args=("quit",user.nick+" "+prefixSuffix[1][1:],0,user,recipient));
							self.console.threads["quit"].start();
							self.removeUser(nick);
					elif (prefixSuffix[0] == "privmsg"):
						# message
						recipient = prefixSuffix[1].split(" ",1)[0];
						message = prefixSuffix[1][prefixSuffix[1].find(":")+1:];
						description = 0;
						if (message[0:8].lower() == u"\001action " and message[-1:] == u"\001"):
							# DESCRIPTION!
							description = 1;
							message = message[8:-1];
						elif (message[0:1] == u"\001" and message[-1:] == u"\001"):
							# CTCP!
							description = 2;
							message = message[1:-1];
						
						if (description > 1):
							eventType = "CTCP";
						elif (description == 1):
							eventType = "DESC";
						else:
							eventType = "MSG";
						
						if (recipient.lower() != self.currentNick.lower() and description >= 2):
							self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=(message,description,user,""));
							self.console.threads["response"].start();
						
						if (recipient.lower() == self.currentNick.lower()):
							if (user != None):
								user.updateLastPrivateMsg();
							self.consoleOutput("PRIV "+nick+" "+eventType+": "+message);
							self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=(message,description,user,""));
							self.console.threads["response"].start();
						else:
							if (user != None):
								user.updateLastPublicMsg();
							self.consoleOutput(recipient+" "+nick+" "+eventType+": "+message);
							if (not description):
								if (message.lower() == "++platopus" and random.random() <= 0.2):
									self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=("i love you",description,user,recipient));
									self.console.threads["response"].start();
								elif (message.lower() == "--platopus" and random.random() <= 0.75):
									self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=("fuck you",description,user,recipient));
									self.console.threads["response"].start();
								
								splitMessage = message.split(" ",1);
								
								if (message[0:1] == "!" and len(message) > 1 and recipient[0:1] == "#" and Settings.SHORT_NOTATION_CHANNELS.count(recipient.lower()) >= 1):
									# shorthand notation enabled
									self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=(message[1:],description,user,recipient));
									self.console.threads["response"].start();
								elif (len(splitMessage) > 1):
									splitMessage[0] = splitMessage[0].lower();
									nameMatch = 0;
									for name in self.RESPONSE_NAMES:
										if (name.lower() == splitMessage[0].lower() or name.lower()+"," == splitMessage[0].lower()):
											nameMatch = 1;
											break;
									
									if (nameMatch or splitMessage[0].lower() == self.currentNick.lower() or splitMessage[0].lower() == self.currentNick.lower()+","):
										self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=(splitMessage[1],description,user,recipient));
										self.console.threads["response"].start();
									elif ((splitMessage[0] == "!hand" or splitMessage[0] == "!pass" or splitMessage[0] == "!lob" or splitMessage[0] == "!chuck" or splitMessage[0] == "!toss" or splitMessage[0] == "!punt" or splitMessage[0] == "!pitch" or splitMessage[0] == "!fling" or splitMessage[0] == "!hurl") and self.console.getVar("lg_target").lower() == user.nick.lower()):
										# lg shorthand response commands
										self.console.threads["response"] = Thread(target=self.responseSystem.callResponse,args=(message[1:],description,user,recipient));
										self.console.threads["response"].start();
									else:
										# not a command... so index it for jabber
										self.console.threads["jabber_index"] = Thread(target=self.responseSystem.callResponseScript,args=("jabberindex",message,description,user,recipient));
										self.console.threads["jabber_index"].start();
								else:
									# not a command... so index it for jabber
									self.console.threads["jabber_index"] = Thread(target=self.responseSystem.callResponseScript,args=("jabberindex",message,description,user,recipient));
									self.console.threads["jabber_index"].start();
					elif (prefixSuffix[0] == "notice"):
						recipient = prefixSuffix[1].split(" ",1)[0];
						message = prefixSuffix[1][prefixSuffix[1].find(":")+1:];
						description = 0;
						if (message[0:1] == u"\001" and message[-1:] == u"\001"):
							# CTCP REPLY!
							description = 2;
							message = message[1:-1];
						
						if (description > 1):
							eventType = "CTCPREPLY";
						else:
							eventType = "NOTICE";
						
						if (recipient.lower() == self.currentNick.lower()):
							self.consoleOutput("PRIV "+nick+" "+eventType+": "+message);
						else:
							self.consoleOutput(recipient+" "+nick+" "+eventType+": "+message);
						
					elif (prefixSuffix[0] == "nick"):
						# nick change
						newNick = prefixSuffix[1][1:];
						
						self.consoleOutput("NICK "+user.nick+"->"+newNick);
						# first, go around and zap anyone who has this existing nick
						self.removeUser(newNick);
						
						# now report it to our response script
						self.console.threads["nick_change"] = Thread(target=self.responseSystem.callResponseScript,args=("nickchange",user.nick+" "+newNick,0,user,recipient));
						self.console.threads["nick_change"].start();
						
						# now adjust the old nick
						user.nick = newNick;
						
						
					elif (prefixSuffix[0] == "kick"):
						channel = prefixSuffix[1].split(" ",2)[0];
						target = prefixSuffix[1].split(" ",2)[1];
						message = prefixSuffix[1].split(" ",2)[2][1:];
						kickedUser = self.getUser(target);
						self.partUserFromChannel(kickedUser, channel);
						if (target.lower() == self.currentNick.lower()):
							self.consoleOutput("Kicked from channel "+channel+" by "+nick+" ("+message+")");
							del self.channels[channel.lower()];
							# auto rejoin crap
							if (Settings.AUTO_REJOIN and self.incrementChannelRejoins(channel.lower())):
								self.joinChannel(channel,1);
						else:
							self.consoleOutput(channel+" "+nick+" KICK "+target+": "+message);
							if (not kickedUser.isStillRelevant()):
								self.removeUser(kickedUser.nick);
					elif (prefixSuffix[0] == "mode"):
						channel = prefixSuffix[1].split(" ",1)[0];
						modes = prefixSuffix[1].split(" ",1)[1];
						self.consoleOutput(channel+" "+nick+" MODE: "+modes);
						modes = modes.split(" ");
						currentTarget = 1;
						plusMinus = 1; # 1 = plus, 0 = minus
						for c in modes[0]:
							if (c == "+"):
								plusMinus = 1;
							elif (c == "-"):
								plusMinus = 0;
							elif (self.PARAMETER_MODES.find(c) >= 0):
								if (len(modes) > currentTarget):
									target = modes[currentTarget];
									if (c == "o"): # someone's being opped/de-opped
										user = self.getUser(target);
										if (user.channels.has_key(channel.lower())):
											user.channels[channel.lower()] = plusMinus;
									currentTarget += 1;
					elif (prefixSuffix[0] == "302"):
						# User host
						#:servercentral.il.us.quakenet.org 302 testestest :iCeD=+~spam@c-24-7-28-123.hsd1
						#.ca.comcast.net
						userHost = prefixSuffix[1].split();
						if (len(userHost) >= 2):
							userHost = userHost[1];
							if (userHost[0:1] == ":"):
								userHost = userHost[1:];
							if (userHost.find("=") >= 0 and userHost.find("@") >= 0):
								userHost = userHost.split("=",1);
								nick = userHost[0];
								userHost = userHost[1].split("@",1);
								ident = userHost[0];
								if (ident[0:1] == "+"):
									ident = ident[1:];
								hostName = userHost[1];
								targetUser = self.getUser(nick);
								if (targetUser != None):
									targetUser.ident = ident;
									targetUser.host = hostName;
									targetUser.checkHostnameRememberance(self.console.fileSystem,self.console);
					elif (prefixSuffix[0] == "353"):
						# NAMES list
						forChannel = prefixSuffix[1].split()[2].lower();
						namesList = prefixSuffix[1][prefixSuffix[1].find(":")+1:].split();
						for name in namesList:
							op = 0;
							if (name[0:1] == "@"):
								op = 1;
								name = name[1:];
							elif (name[0:1] == "+"):
								name = name[1:];
							user = self.getUser(name);
							if (user == None):
								user = User(name, "", "");
							self.joinUserToChannel(user,forChannel);
							if (op):
								user.opOnChannel(forChannel);
							self.userHost(user.nick);
							#self.channels[forChannel].append(user);
					elif (prefixSuffix[0] == "404"):
						# can't send to channel
						channel = prefixSuffix[1].split(" ",2)[1];
						self.consoleOutput("Cannot send to channel "+channel);
					elif (prefixSuffix[0] == "471"):
						# full channel
						channel = prefixSuffix[1].split(" ",2)[1];
						self.consoleOutput("Cannot join "+channel+" (channel is full).");
						# auto rejoin crap
						if (Settings.AUTO_REJOIN and self.incrementChannelRejoins(channel.lower())):
							self.setAutoRejoinTimer(channel);
					elif (prefixSuffix[0] == "473"):
						# invite only
						channel = prefixSuffix[1].split(" ",2)[1];
						self.consoleOutput("Cannot join "+channel+" (channel is invite-only).");
						# auto rejoin crap
						if (Settings.AUTO_REJOIN and self.incrementChannelRejoins(channel.lower())):
							self.setAutoRejoinTimer(channel);
					elif (prefixSuffix[0] == "474"):
						# BANNED
						channel = prefixSuffix[1].split(" ",2)[1];
						self.consoleOutput("Cannot join "+channel+" (banned from channel).");
						# auto rejoin crap
						if (Settings.AUTO_REJOIN and self.incrementChannelRejoins(channel.lower())):
							self.setAutoRejoinTimer(channel);
					elif (prefixSuffix[0] == "475"):
						# passworded
						channel = prefixSuffix[1].split(" ",2)[1];
						self.consoleOutput("Cannot join "+channel+" (correct key needed).");
						# auto rejoin crap
						if (Settings.AUTO_REJOIN and self.incrementChannelRejoins(channel.lower())):
							self.setAutoRejoinTimer(channel);
				else:
					#print "got from "+nick+" ("+ident+"--"+hostname+"): "+line;
					pass;
	
	def joinChannel(self, channelName, isRejoinAttempt = 0):
		""" Joins a channel. """
		if ( not self.channels.has_key(channelName.lower()) ):
			if (isRejoinAttempt):
				self.consoleOutput("Attempting to rejoin channel "+channelName+" (attempt "+str(self.channelRejoins[channelName.lower()])+"/"+str(Settings.AUTO_REJOIN_MAX_ATTEMPTS)+")...");
			self.sendLine("JOIN "+channelName);
	
	def partChannel(self, channelName, message = ""):
		""" Parts a channel. """
		if ( self.channels.has_key(channelName.lower()) ):
			if (message != ""):
				self.sendLine("PART "+channelName+" :"+message);
			else:
				self.sendLine("PART "+channelName);
	
	def sendMsg(self, recipient, message = "", messagesInChain = 1):
		if (message != "" and self.connected and messagesInChain <= self.MAX_MESSAGES_PER_REQUEST):
			while (len(self.messageTimes) >= self.MESSAGE_FLOOD_LIMIT[0] and self.messageTimes[0] >= time()-self.MESSAGE_FLOOD_LIMIT[1]):
				sleep(0.001);
			remainder = "";
			if (len(message) > self.MAX_MESSAGE_LEN):
				remainder = message[self.MAX_MESSAGE_LEN:];
				message = message[0:self.MAX_MESSAGE_LEN];
			self.sendLine("PRIVMSG "+recipient+" :"+message);
			self.consoleOutput(recipient+" SEND-MSG: "+message);
			self.messageTimes.append(time());
			if (len(self.messageTimes) > self.MESSAGE_FLOOD_LIMIT[0]):
				self.messageTimes = self.messageTimes[1:];
			if (remainder != ""):
				self.sendMsg(recipient,remainder,messagesInChain + 1); # send remainder
	
	def sendDesc(self, recipient, message = "", messagesInChain = 1):
		if (message != "" and self.connected and messagesInChain <= self.MAX_MESSAGES_PER_REQUEST):
			while (len(self.messageTimes) >= self.MESSAGE_FLOOD_LIMIT[0] and self.messageTimes[0] >= time()-self.MESSAGE_FLOOD_LIMIT[1]):
				sleep(0.001);
			remainder = "";
			if (len(message) > self.MAX_MESSAGE_LEN):
				remainder = message[self.MAX_MESSAGE_LEN:];
				message = message[0:self.MAX_MESSAGE_LEN];
			self.sendLine(u"PRIVMSG "+recipient+" :\001ACTION "+message+u"\001");
			self.consoleOutput(recipient+" SEND-DESC: "+message);
			self.messageTimes.append(time());
			if (len(self.messageTimes) > self.MESSAGE_FLOOD_LIMIT[0]):
				self.messageTimes = self.messageTimes[1:];
			if (remainder != ""):
				self.sendDesc(recipient,remainder,messagesInChain + 1); # send remainder
			
	def sendNotice(self, recipient, message = "", messagesInChain = 1):
		if (message != "" and self.connected and messagesInChain <= self.MAX_MESSAGES_PER_REQUEST):
			while (len(self.messageTimes) >= self.MESSAGE_FLOOD_LIMIT[0] and self.messageTimes[0] >= time()-self.MESSAGE_FLOOD_LIMIT[1]):
				sleep(0.001);
			remainder = "";
			if (len(message) > self.MAX_MESSAGE_LEN):
				remainder = message[self.MAX_MESSAGE_LEN:];
				message = message[0:self.MAX_MESSAGE_LEN];
			self.sendLine("NOTICE "+recipient+" :"+message);
			self.consoleOutput(recipient+" SEND-NOTICE: "+message);
			self.messageTimes.append(time());
			if (len(self.messageTimes) > self.MESSAGE_FLOOD_LIMIT[0]):
				self.messageTimes = self.messageTimes[1:];
			if (remainder != ""):
				self.sendDesc(recipient,remainder,messagesInChain + 1); # send remainder
	
	def kickUser(self, channel, nick, reason):
		if (self.connected):
			self.sendLine("KICK "+channel+" "+nick+" :"+reason);
	
	def setMode(self, mode):
		if (self.connected):
			self.sendLine("MODE "+mode);
	
	def userHost(self, nick):
		if (self.connected):
			self.sendLine("USERHOST "+nick);
	
	def disconnect(self, quitMessage = ""):
		if (self.connected):
			if (quitMessage == ""):
				quitMessage = self.quitMessage;
			if (quitMessage == ""):
				self.sendLine("QUIT");
			else:
				self.sendLine("QUIT :"+quitMessage);
			
			self.channels = {};
			self.users = [];
			self.connected = 0;
			self.connecting = 0;
			#self.close();
			
			self.consoleOutput("Disconnected from "+self.currentServer+".");