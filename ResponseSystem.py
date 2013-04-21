# -*- coding: utf-8 -*-
########################################
# platopus response system class
########################################
#
# This handles all responses from messages sent
# to the bot.

import os; # os-level functions
import hashlib; # hash functions
from Utility import normalize, getOutcome, strMerge, toFormattedTime, fromFormattedTime;
import random;

class ResponseSystem:
	
	INDEX_FILE = os.path.join(".","ResponseIndex.py");
	SCRIPTS_DIR = "response";
	
	def __init__(self):
		self.scripts = {};
		self.hashes = {};
		
		self.scriptIndex = "";
		self.scriptIndexHash = "";
		
		self.console = None;
		self.connection = None;
		self.fileSystem = None;
		
		# jabber stuff
		self.jabberNGrams = {}; # channel/nick is key, words are subkeys, joining words are listed
		
		self.globalEncoreHistory = [];
		self.channelEncoreHistory = {};
	
	def refreshIndex(self):
		""" Refreshes the response script index. """
		try:
			indexFile = open(self.INDEX_FILE,"r");
			self.scriptIndex = indexFile.read();
			self.scriptIndexHash = hashlib.md5(self.scriptIndex).digest();
			indexFile.close();
		except IOError:
			self.console.output("Could not reload index. File IO error.");
	
	def refreshScript(self, script):
		try:
			scriptFile = open(os.path.join(".",self.SCRIPTS_DIR,script+".py"),"r");
			self.scripts[script] = scriptFile.read();
			#self.scripts[script] = "\t\t"+self.scripts[script];
			#self.scripts[script] = self.scripts[script].replace("\r","\r\t\t");
			#self.scripts[script] = self.scripts[script].replace("\n","\n\t\t");
			self.hashes[script] = hashlib.md5(self.scripts[script]).digest();
			scriptFile.close();
		except IOError:
			self.console.output("Could not reload response file. File IO error.");
	
	def consoleOutput(self, text):
		""" Checks to see that the console object exists and if so, outputs a line to it """
		if (self.console != None):
			self.console.output(text);
	
	def getRecipient(self, user, channel = ""):
		""" Names the proper recipient of a response. """
		if (channel == ""):
			return user.getIdentity();
		else:
			return channel;
	
	def nameBeginning(self, user, channel = ""):
		""" If necessary, returns Name: at the beginning of a message. """
		if (channel != ""):
			return ""+user.getIdentity()+": ";
		else:
			return "";
	
	def parse(self, line, target, user, channel = ""):
		if (target.strip() == "" and channel.strip() != ""):
			target = channel;
		elif (target.strip() == ""):
			target = user.getIdentity();
		elif (target == "me"):
			target = user.getIdentity();
		elif (target == "you"):
			target = self.connection.currentNick;
		line = line.replace("{them}",user.getIdentity());
		line = line.replace("{theirnick}",user.nick);
		line = line.replace("{chan}",channel);
		if (target != None):
			print target;
			line = line.replace("{target}",target);
		else:
			line = line.replace("{target}","");
		return line;
	
	def parseNGram(self, contents):
		nGram = {};
		for line in contents:
			splitLine = line.split(" ",1);
			if (not nGram.has_key(splitLine[0])):
				nGram[splitLine[0]] = [];
			
			if (len(splitLine) < 2):
				nGram[splitLine[0]].append("");
			else:
				nGram[splitLine[0]].append(splitLine[1]);
		return nGram;
	
	
	def addNGram(self, nGram, line):
		""" Adds traces of a line to an existing n-gram """
		line = line.split(" ");
		for i in range(0,len(line)):
			word = line[i].lower();
			if (not nGram.has_key(word)):
				nGram[word] = [];
			
			if (i+1 < len(line)):
				following = line[i+1:];
				nGram[word].append(following);
			else:
				nGram[word.lower()].append([]);
		return nGram;
	
	def removeNGram(self, nGram, line):
		""" Removes traces of a line from an existing n-gram """
		line = line.split(" ");
		for i in range(0,len(line)):
			word = line[i].lower();
			if (nGram.has_key(word)):
				if (i+1 < len(line)):
					nextWord = line[i+1:];
					nGram[word].remove(nextWord);
				else:
					nGram[word.lower()].remove([]);
				if (len(nGram[word]) <= 0):
					del nGram[word];
		return nGram;
			
	
	def callResponse(self, command, isDescription, user, channel = "", logForEncore = 1):
		""" Calls a generic response. """
		if (self.scriptIndexHash == hashlib.md5(self.scriptIndex).digest()):
			exec(self.scriptIndex);
		else:
			self.consoleOutput("Hash-Script mismatch on response index.");
	
	def callResponseScript(self, script, command, isDescription, user, channel = "", parameters = {}):
		""" Calls a script-specific response. """
		if (not self.scripts.has_key(script)):
			self.refreshScript(script);
		if (self.scripts.has_key(script) and self.hashes.has_key(script)):
			if (self.hashes[script] == hashlib.md5(self.scripts[script]).digest()):
				exec(self.scripts[script]);
			else:
				self.consoleOutout("Hash-Script mismatch on script '"+script+"'.");
	
	def isInChannel(self, nick, channel):
		# tests if nick is on channel. If yes, return the user object. If no, return None.
		user = self.connection.getUser(nick);
		if (user == None):
			return None;
		if (user.channels.has_key(channel.lower())):
			return user;
		else:
			return None;
	
	def isOpInChannel(self, nick, channel):
		# tests if a nick is on a channel and if he/she is opped. If yes, return the user object. If no, return None.
		user = self.connection.getUser(nick);
		if (user == None):
			return None;
		if (user.channels.has_key(channel.lower()) and user.channels[channel.lower()]):
			return user;
		else:
			return None;
	
	def checkPointRequirement(self, user, channel, points, action = "perform this action"):
		if (not user.isLoggedIn()):
			if (points > 0):
				self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+"You must be logged in and have at least "+str(points)+" available points to "+action+".");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+"You must be logged in to "+action+".");
			ACCOUNT_REGISTER_NOTICE = "If you have not registered an account with me, you may do so by using the command /msg "+self.connection.currentNick+" createaccount and following the instructions.";
			if (channel != ""):
				self.connection.sendNotice(user.nick,ACCOUNT_REGISTER_NOTICE);
			else:
				self.connection.sendMsg(user.nick,ACCOUNT_REGISTER_NOTICE);
			return 0;
		elif (user.availablePoints < points):
			self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+"You need at least "+str(points)+" available points to "+action+".");
			return 0;
		else:
			user.deductPoints(points);
			return 1;