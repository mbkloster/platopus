########################################
# platopus console class
########################################
#
# Represents platopus's console screen, which interpets
# and uses all commands given locally, as well as
# outputs stuff from the irc input.

from time import time, strftime, localtime, sleep;
from Utility import getSuffixFromList;
from threading import Thread, Timer;
from Connection import Connection;
from ResponseSystem import ResponseSystem;
from FileSystem import FileSystem;
from Settings import Settings;
import random;
import sys; # system functions
import os;

class Console:

	dateFormat = "%a %b %d %Y";
	timeFormat = "%H:%M:%S";
	completeDateFormat = "%a %b %d %Y %H:%M:%S";
	variableFile = os.path.join(".","misc","variables.txt");
	
	NOT_CONNECTED_MSG = "Not connected to server.";
	
	class RandomGenerator:
		REROLL_CHANCES = (1.00, 0.96, 0.94, 0.85, 0.70, 0.60);
		MAX_REROLLS = 8;
		HISTORY_LEN = 30;
		
		def __init__(self):
			self.rollHistory = []; # in form (lower,upper,result)
		
		def randInt(self, lowerBound, upperBound):
			result = None;
			done = 0;
			rerolls = 0;
			while (not done):
				result = random.randint(lowerBound,upperBound);
				boundMatches = 0;
				done = 1;
				for roll in self.rollHistory:
					if (roll[0] == lowerBound and roll[1] == upperBound):
						boundMatches += 1;
					if (roll[2] == result and boundMatches < len(self.REROLL_CHANCES) and random.random() < self.REROLL_CHANCES[boundMatches-1] and rerolls < self.MAX_REROLLS):
						done = 0;
						rerolls += 1;
						break;
			self.rollHistory = [[lowerBound,upperBound,result],] + self.rollHistory;
			return result;
	
	def __init__(self, logFile):
		self.lastDate = "";
		self.lastLogDate = "";
		
		self.logFile = logFile;
		self.active = 1;
		
		self.threads = {}; # threads and timers
		self.connection = None;
		
		self.fileSystem = FileSystem(self);
		
		self.responseSystem = ResponseSystem();
		self.responseSystem.console = self;
		self.responseSystem.refreshIndex();
		self.responseSystem.fileSystem = self.fileSystem;
		
		self.reconnectAttempts = 0;
		
		self.random = self.RandomGenerator();
		
		self.reloadVariables();
	
	def saveVariables(self):
		""" Saves all of the bot's variables. """
		fileLines = [];
		for varName, varValue in self.variables.items():
			if (varValue != "" and varValue != ""):
				if (type(varValue) == str):
					fileLines.append(varName+" \""+varValue+"\"");
				else:
					fileLines.append(varName+" "+str(varValue));
		self.fileSystem.save(self.variableFile,fileLines);
	
	def reloadVariables(self):
		""" Reloads all of the bot's variables directly from the file. """
		self.variables = {};
		variableFile = self.fileSystem.getFileContents(self.variableFile,0);
		for variableLine in variableFile:
			variableLine = variableLine.split(" ",1);
			if (len(variableLine) > 1):
				self.variables[variableLine[0]] = variableLine[1];
				if (self.variables[variableLine[0]][0:1] == "\"" and self.variables[variableLine[0]][-1:] == "\""):
					self.variables[variableLine[0]] = self.variables[variableLine[0]][1:-1];
				else:
					try:
						if (self.variables[variableLine[0]].count(".")):
							self.variables[variableLine[0]] = float(self.variables[variableLine[0]]);
						else:
							self.variables[variableLine[0]] = int(self.variables[variableLine[0]]);
					except ValueError:
						del(self.variables[variableLine[0]]);
			if (self.variables.has_key(variableLine[0]) and self.variables[variableLine[0]] == ""):
				del self.variables[variableLine[0]];
	
	def getVar(self, varName):
		if (self.variables.has_key(varName)):
			return self.variables[varName];
		else:
			return "";
	
	def setVar(self, varName, varValue):
		if (self.variables.has_key(varName) and varValue == ""):
			del self.variables[varName];
		else:
			self.variables[varName] = varValue;
		self.saveVariables();
	
	def hasThread(self, timerName):
		if (self.threads.has_key(timerName)):
			if (self.threads[timerName] != None):
				return 1;
			else:
				return 0;
		else:
			return 0;
	
	def createConnection(self):
		""" Creates a new connection object. Should be called prior to connecting. """
		self.connection = Connection(Settings.NICKS, Settings.LOGIN_USER, Settings.LOGIN_DOMAIN, Settings.LOGIN_REAL_NAME, Settings.IRC_SERVER, Settings.IRC_PORT);
		self.connection.console = self;
		self.connection.quitMessage = Settings.QUIT_MESSAGE;
		self.connection.autoJoinChannels = Settings.AUTO_JOIN_CHANNELS;
		self.connection.responseSystem = self.responseSystem;
		self.responseSystem.connection = self.connection;
	
	def reconnect(self):
		""" Reconnects after a disconnection """
		self.reconnectAttempts += 1;
		while ((self.connection == None or not self.connection.connected) and self.reconnectAttempts <= Settings.MAX_AUTO_RECONNECT_ATTEMPTS):
			self.output("Automatically reconnecting in "+str(Settings.AUTO_RECONNECT_DELAY)+" seconds (attempt "+str(self.reconnectAttempts)+"/"+str(Settings.MAX_AUTO_RECONNECT_ATTEMPTS)+")...");
			sleep(Settings.AUTO_RECONNECT_DELAY);
			self.createConnection();
			if (self.connection.IRCConnect()):
				self.reconnectAttempts = 0;
				break;
			elif (self.reconnectAttempts >= 1):
				self.reconnectAttempts += 1;
	
	def sessionStart(self, timestamp = time()):
		print "[Session Start: "+strftime(self.completeDateFormat,localtime(timestamp))+"]";
		self.log("[Session Start: "+strftime(self.completeDateFormat,localtime(timestamp))+"]",timestamp,0);
	
	def sessionEnd(self, timestamp = time()):
		print "[Session End: "+strftime(self.completeDateFormat,localtime(timestamp))+"]";
		self.log("[Session End: "+strftime(self.completeDateFormat,localtime(timestamp))+"]",timestamp,0);
		self.active = 0;
	
	def log(self, text, timestamp, includeTime = 1):
		""" Logs a line to the log file. """
		file = open(self.logFile,"a");
		if (file != None):
			date = strftime(self.dateFormat,localtime(timestamp));
			if (date != self.lastLogDate):
				file.write("[Date: "+date+"]\r\n");
				self.lastLogDate = date;
			
			if (includeTime):
				file.write("["+strftime(self.timeFormat,localtime(timestamp))+"] "+text+"\r\n");
			else:
				file.write(text+"\r\n");
	
	def output(self, text, log = 1):
		""" Outputs a line to the console. """
		timestamp = time();
		date = strftime(self.dateFormat,localtime(timestamp));
		if (date != self.lastDate):
			print "\n[Date: "+date+"]";
			self.lastDate = date;
		print "["+strftime(self.timeFormat,localtime(timestamp))+"] "+text;
		if (log):
			self.log(text,timestamp);
	
	def adjustDate(self, timestamp = time()):
		""" Adjusts the current date. By default, uses the current time on the system. """
		date = strftime(self.dateFormat,localtime(timestamp));
		self.lastDate = date;
		self.lastLogDate = date;
	
	def send(self, command):
		""" Sends a command to the interpreter, usually from input. """
		self.log("> "+command,time());
		lowerCommand = command.lower();
		prefixSuffix = getSuffixFromList(command,lowerCommand,("reloadresponse","reloadresponseindex","quit","connect","disconnect","join","part","kick","mode","msg","desc","uncache","listusers","setvar","getvar","raw"));
		if (prefixSuffix != None):
			if (prefixSuffix[0] == "reloadresponse"):
				# reload response script
				if (len(prefixSuffix) > 1):
					self.output("Reloading response script '"+prefixSuffix[1]+"'...");
					self.responseSystem.refreshScript(prefixSuffix[1]);
				else:
					self.output("Not enough parameters. Format: reloadresponse [script]");
			elif (prefixSuffix[0] == "reloadresponseindex"):
				self.output("Reloading response index...");
				self.responseSystem.refreshIndex();
			elif (prefixSuffix[0] == "quit"):
				# quit out
				if (self.connection != None and (self.connection.connected or self.connection.connecting)):
					self.connection.disconnect(prefixSuffix[1]);
					sleep(0.25);
				self.output("Goodbye, son.");
				self.active = 0;
			elif (prefixSuffix[0] == "connect"):
				# connect to server
				if (self.connection == None):
					self.createConnection();
				if (not self.connection.connected):
					self.createConnection();
					self.threads["connect"] = Thread(target=self.connection.IRCConnect);
					self.threads["connect"].setDaemon(1);
					self.threads["connect"].start();
				else:
					self.output("Already connected to server.");
			elif (prefixSuffix[0] == "disconnect"):
				if (self.connection != None and (self.connection.connected or self.connection.connecting)):
					self.connection.disconnect(prefixSuffix[1]);
				else:
					self.output(self.NOT_CONNECTED_MSG);
			elif (prefixSuffix[0] == "join"):
				if (self.connection != None and self.connection.connected):
					self.connection.joinChannel(prefixSuffix[1]);
				else:
					self.output(self.NOT_CONNECTED_MSG);
			elif (prefixSuffix[0] == "part"):
				if (self.connection != None and self.connection.connected):
					if (prefixSuffix[1].find(" ") < 0):
						# no parting message
						self.connection.partChannel(prefixSuffix[1]);
					else:
						# parting message!
						channel = prefixSuffix[1].split(" ",1)[0];
						message = prefixSuffix[1].split(" ",1)[1];
						self.connection.partChannel(channel,message);
				else:
					self.output(self.NOT_CONNECTED_MSG);
			elif (prefixSuffix[0] == "msg"):
				if (len(prefixSuffix[1].split(" ",1)) > 1):
					recipient = prefixSuffix[1].split(" ",1)[0];
					message = prefixSuffix[1].split(" ",1)[1];
					if (self.connection != None and self.connection.connected):
						self.connection.sendMsg(recipient, message);
					else:
						self.output(self.NOT_CONNECTED_MSG);
				else:
					self.output("Not enough parameters. Format: msg [recipient] [message]");
			elif (prefixSuffix[0] == "desc"):
				if (len(prefixSuffix[1].split(" ",1)) > 1):
					recipient = prefixSuffix[1].split(" ",1)[0];
					message = prefixSuffix[1].split(" ",1)[1];
					if (self.connection != None and self.connection.connected):
						self.connection.sendDesc(recipient, message);
					else:
						self.output(self.NOT_CONNECTED_MSG);
				else:
					self.output("Not enough parameters. Format: desc [recipient] [message]");
			elif (prefixSuffix[0] == "uncache"):
				self.fileSystem.uncache(prefixSuffix[1]);
				self.output("Uncaching file "+prefixSuffix[1]+"...");
			elif (prefixSuffix[0] == "listusers"):
				if (self.connection != None and self.connection.connected):
					if (len(prefixSuffix) <= 1 or prefixSuffix[1].strip() == ""):
						self.output("Global users:");
						for user in self.connection.users:
							self.output(user.nick+" "+user.ident+"@"+user.host);
							channels = user.channels.items();
							for channel, opped in user.channels.items():
								if (opped):
									self.output("@"+channel);
								else:
									self.output(channel);
					else:
						channel = prefixSuffix[1].strip().lower();
						if (self.connection.channels.has_key(channel)):
							self.output("Users in "+channel+":");
							for user in self.connection.channels[channel]:
								if (user.channels.has_key(channel) and user.channels[channel]):
									self.output("@"+user.nick+" "+user.ident+"@"+user.host);
								elif (user.channels.has_key(channel)):
									self.output(user.nick+" "+user.ident+"@"+user.host);
								else:
									self.output("$"+user.nick+" "+user.ident+"@"+user.host);
						else:
							self.output("Unknown channel "+channel);
				else:
					self.output("Not connected to server.");
			elif (prefixSuffix[0] == "mode"):
				self.connection.setMode(prefixSuffix[1]);
			elif (prefixSuffix[0] == "kick"):
				if (self.connection != None and self.connection.connected):
					parameters = prefixSuffix[1].split(" ",2);
					if (len(parameters) >= 3):
						self.connection.kickUser(parameters[0],parameters[1],parameters[2]);
					else:
						self.output("Usage: kick [channel] [user] [reason]");
			elif (prefixSuffix[0] == "getvar"):
				var = self.getVar(prefixSuffix[1]);
				if (var != ""):
					if (type(var) == str):
						self.output(prefixSuffix[1]+"=\""+var+"\"");
					else:
						self.output(prefixSuffix[1]+"="+str(var));
				else:
					self.output("Variable '"+prefixSuffix[1]+"' not set");
			elif (prefixSuffix[0] == "setvar"):
				varSet = prefixSuffix[1].split(" ",1);
				if (len(varSet) >= 2):
					try:
						if (varSet[1][0:1] == "\"" and varSet[1][-1:] == "\""): # string value
							self.setVar(varSet[0],varSet[1][1:-1]);
							self.output("Set '"+varSet[0]+"' to "+varSet[1]);
						elif (varSet[1].find(".") >= 0): # float value
							value = float(varSet[1]);
							self.setVar(varSet[0],value);
							self.output("Set '"+varSet[0]+"' to "+str(value));
						else: # integer value
							value = int(varSet[1]);
							self.setVar(varSet[0],value);
							self.output("Set '"+varSet[0]+"' to "+str(value));
					except ValueError:
						self.output("Could not set variable '"+varSet[0]+"' due to a value error - bad input?");
				else:
					self.output("Usage: setvar [variable name] [value]");
			elif (prefixSuffix[0] == "raw"):
				if (self.connection != None and self.connection.connected):
					self.connection.sendLine(prefixSuffix[1]);
				else:
					self.output(self.NOT_CONNECTED_MSG);
		else:
			self.output("Unrecognized command.");