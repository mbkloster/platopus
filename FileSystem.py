########################################
# platopus file system class
########################################
#
# Manages files, particularly ones that
# will be accessed during things like rsg
# and other random-line commands.

import re;
from threading import Timer;
import random;
from time import time;

class FileSystem:
	
	# File cache timeout (in seconds).
	FILE_CACHE_TIMEOUT = 1200;
	
	def __init__(self, console):
		self.files = {};
		self.fileTimers = {};
		self.console = console;
	
	def uncache(self, fileName):
		if (self.files.has_key(fileName)):
			del self.files[fileName];
		if (self.fileTimers.has_key(fileName)):
			self.fileTimers[fileName].cancel();
			del self.fileTimers[fileName];
	
	def getFileContents(self, fileName, useCaching = 1):
		if (useCaching and self.files.has_key(fileName)):
			return self.files[fileName];
		else:
			try:
				file = open(fileName,"r");
				contents = file.read();
				contents = contents.replace("\r\n","\n");
				contents = contents.replace("\n\r","\n");
				contents = contents.replace("\r","\n");
				file.close();
				contents = contents.split("\n");
			except IOError:
				contents = None;
			if (useCaching and contents != None):
				self.files[fileName] = contents;
				self.fileTimers[fileName] = Timer(self.FILE_CACHE_TIMEOUT,self.uncache,(fileName,));
				self.fileTimers[fileName].setDaemon(1);
				self.fileTimers[fileName].start();
			return contents;
	
	def getLineCount(self, fileName, useCaching = 1):
		return len(self.getFileContents(fileName, useCaching));
	
	def getLine(self, fileName, lineNumber, useCaching = 1):
		""" Grabs a specific file from the file contents """
		contents = self.getFileContents(fileName,useCaching);
		if (len(contents) > lineNumber and lineNumber >= 0):
			return contents[lineNumber];
		else:
			return "";
	
	def getRandomLine(self, fileName, useCaching = 1):
		""" Grabs a specific file from the file contents """
		contents = self.getFileContents(fileName,useCaching);
		if (len(contents) > 0):
			return contents[self.console.random.randInt(0,len(contents)-1)];
		else:
			return "";
	
	def save(self, fileName, fileContents = None):
		""" Saves over a file. If fileContents = None, use cached version """
		if (fileContents == None):
			if (self.files[fileName] == None):
				print "NO FILE CONTENTS";
				return 0;
			else:
				fileContents = self.files[fileName];
		elif (fileContents != None and self.files.has_key(fileName)): # If we have an existing cached version of the file... update
			self.files[fileName] = fileContents;
		
		#try:
		file = open(fileName,"w");
		first = 1;
		for line in fileContents:
			if (not first):
				file.write("\r\n"+line);
			else:
				file.write(line);
				first = 0;
		file.close();
		#except IOError:
		#	return 0;
		return 1;