########################################
# platopus response index file
########################################
#
# The main evaluated code for the response index.
# This is NOT meant to be executed by itself, but
# rather, as part of ResponseSystem.
import random;

from Utility import getSuffixFromList;
from time import strftime;

if (isDescription >= 2):
	ctcpPS = getSuffixFromList(command,command.lower(),["ping","version","time","finger"]);
	if (ctcpPS != None):
		if (ctcpPS[0] == "ping"):
			self.connection.sendNotice(user.nick,u"\001PING "+ctcpPS[1]+u"\001");
		elif (ctcpPS[0] == "version"):
			self.connection.sendNotice(user.nick,u"\001VERSION I am a product of evolutionary biology, and the tutelage of the philosopher Socrates.\001");
		elif (ctcpPS[0] == "time"):
			self.connection.sendNotice(user.nick,u"\001TIME "+strftime("%A, %B %d %Y %H:%M:%S")+u"\001");
		elif (ctcpPS[0] == "finger"):
			self.connection.sendNotice(user.nick,u"\001FINGER lickin' good\001");
else:
	# targetted commands
	lowerCommand = command.lower();
	targettedPS = getSuffixFromList(command,lowerCommand,["encore","commands","help","garble","imply","praise","fight","jabber","rsg","rsgsource","quote","lg","hand","pass","lob","chuck","toss","punt","pitch","fling","hurl","!hand","!pass","!lob","!chuck","!toss","!punt","!pitch","!fling","!hurl","redirect","8ball","spin","fuck","love you","i love you","love","kiss","why","hello","shup","shutup","unshup","unshutup","kick","rankick","tickbot","monobot","q","whois","whoami","editprofile","accounthelp","managehosts","login","logout","changepassword","createaccount","stealth","is"]);
	
	if (targettedPS != None and not isDescription):
		# targeted responses
		
		# female exceptions for imply/praise
		femaleExceptions = ["barbara streisand","barbara walters","britney spears","enola gay","helen thomas","hillary clinton","janet reno","jeniffer lopez","jenna haze","latoya jackson","marilyn monroe","martha stewart","michelle obama","my mom","princess diana","princess leia","queen elizabeth","sandra day o'connor","sarah palin","some cheap prostitute","vannah white","whitney houston","your mom",];
		if (targettedPS[0] != "encore"):
			if (logForEncore):
				MAX_GLOBAL_HISTORY_LEN = 10; # max history items to store
				MAX_CHANNEL_HISTORY_LEN = 5; # max channel-based history items to store
				self.globalEncoreHistory.append(command);
				if (channel != ""):
					self.channelEncoreHistory[channel.lower()].append(command);
					if (len(self.channelEncoreHistory[channel.lower()]) > MAX_CHANNEL_HISTORY_LEN):
						self.channelEncoreHistory[channel.lower()] = self.channelEncoreHistory[channel.lower()][1:];
				if (user != None):
					user.addToEncoreHistory(command);
				if (len(self.globalEncoreHistory) > MAX_GLOBAL_HISTORY_LEN):
					self.globalEncoreHistory = self.globalEncoreHistory[1:];
			
			if (targettedPS[0] == "fuck"):
				if (targettedPS[1].lower().strip() == "you" or targettedPS[1].lower().strip() == "you." or targettedPS[1].lower().strip() == "you!"):
					self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+self.fileSystem.getRandomLine(os.path.join(".","misc","fuckyou.txt")));
				else:
					self.connection.sendDesc( self.getRecipient(user,channel), self.parse(self.fileSystem.getRandomLine(os.path.join(".","misc","fuck.txt")),targettedPS[1],user,channel) );
			elif (targettedPS[0] == "garble"):
				self.callResponseScript("garble",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "imply"):
				target = targettedPS[1];
				if (target.lower().strip() == "me"):
					target = user.getIdentity();
				elif (target.strip() == ""):
					channelUsers = self.connection.channels[channel.lower()];
					target = channelUsers[random.randint(0,len(channelUsers)-1)];
					target = target.getIdentity();
				possibleUser = self.connection.getUser(target);
				gender = "m";
				if (possibleUser != None and possibleUser.isLoggedIn()):
					gender = possibleUser.gender;
				else:
					if (target.find(" ") < 0):
						userFile = self.fileSystem.getFileContents(os.path.join("accounts",target.lower()+".txt"),0);
						if (userFile != None and len(userFile) >= 12):
							gender = userFile[11];
				
				if (gender != "f"):
					isFemale = femaleExceptions.count(target.lower());
					if (isFemale):
						gender = "f";
				line = self.fileSystem.getRandomLine(os.path.join(".","misc","imply.txt"));
				if (gender == "m" or gender == "n"):
					line = line.replace("_","his");
					line = line.replace("+","he");
				else:
					line = line.replace("+","she");
					line = line.replace("_","her");
				self.connection.sendMsg( self.getRecipient(user,channel), ""+target+" "+line);
			elif (targettedPS[0] == "praise"):
				target = targettedPS[1];
				if (target.lower().strip() == "me"):
					target = user.getIdentity();
				elif (target.strip() == ""):
					channelUsers = self.connection.channels[channel.lower()];
					target = channelUsers[random.randint(0,len(channelUsers)-1)];
					target = target.getIdentity();
				possibleUser = self.connection.getUser(target);
				gender = "m";
				if (possibleUser != None and possibleUser.isLoggedIn()):
					gender = possibleUser.gender;
				else:
					if (target.find(" ") < 0):
						userFile = self.fileSystem.getFileContents(os.path.join("accounts",target.lower()+".txt"),0);
						if (userFile != None and len(userFile) >= 12):
							gender = userFile[11];
				if (gender != "f"):
					isFemale = femaleExceptions.count(target.lower());
					if (isFemale):
						gender = "f";
				line = self.fileSystem.getRandomLine(os.path.join(".","misc","praise.txt"));
				if (gender == "m" or gender == "n"):
					line = line.replace("_","his");
					line = line.replace("+","he");
				else:
					line = line.replace("+","she");
					line = line.replace("_","her");
				self.connection.sendMsg( self.getRecipient(user,channel), ""+target+" "+line);
			elif (targettedPS[0] == "love you" or targettedPS[0] == "i love you"):
				self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+self.fileSystem.getRandomLine(os.path.join(".","misc","loveyou.txt")));
			elif (targettedPS[0] == "love"):
				self.connection.sendDesc( self.getRecipient(user,channel), self.parse(self.fileSystem.getRandomLine(os.path.join(".","misc","love.txt")),targettedPS[1],user,channel) );
			elif (targettedPS[0] == "kiss"):
				self.connection.sendDesc( self.getRecipient(user,channel), self.parse(self.fileSystem.getRandomLine(os.path.join(".","misc","kiss.txt")),targettedPS[1],user,channel) );
			elif (targettedPS[0] == "8ball"):
				self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+self.fileSystem.getRandomLine(os.path.join(".","misc","8ball.txt")));
			elif (targettedPS[0] == "fight"):
				self.callResponseScript("fight",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "hello"):
				self.callResponseScript("hello",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "tickbot"):
				self.connection.sendMsg(self.getRecipient(user,channel),"Ah, yes, the old tales of long ago speak of the myth of such a bot. Pity it never existed.");
			elif (targettedPS[0] == "monobot"):
				self.connection.sendMsg(self.getRecipient(user,channel),"Peaceful co-existence. That's all I want from him.");
			elif (targettedPS[0] == "q"):
				self.connection.sendMsg(self.getRecipient(user,channel),"A bit of an pompous dickhead... but I can live with him.");
			elif (targettedPS[0] == "why"):
				self.connection.sendMsg(self.getRecipient(user,channel),self.nameBeginning(user,channel)+self.parse(self.fileSystem.getRandomLine(os.path.join(".","misc","why.txt")),targettedPS[1],user,channel));
			elif (targettedPS[0] == "spin"):
				if (channel != ""):
					target = self.connection.channels[channel.lower()][random.randint(0,len(self.connection.channels[channel.lower()])-1)];
					self.connection.sendMsg(channel,"11"+user.getIdentity()+" 10spins the bottle, which spins...");
					self.connection.sendMsg(channel,"10...and then lands on 11"+target.getIdentity()+"10. "+self.parse(self.fileSystem.getRandomLine(os.path.join(".","misc","spin.txt")),target.getIdentity(),user,channel));
				else:
					self.connection.sendMsg(user.nick,"You must use this command on a channel.");
			elif (targettedPS[0] == "rsgsource"):
				self.callResponseScript("rsgsource",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "quote"):
				self.callResponseScript("quote",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "lg" or targettedPS[0] == "hand" or targettedPS[0] == "pass" or targettedPS[0] == "lob" or targettedPS[0] == "chuck" or targettedPS[0] == "toss" or targettedPS[0] == "punt" or targettedPS[0] == "pitch" or targettedPS[0] == "fling" or targettedPS[0] == "hurl" or targettedPS[0] == "redirect" or targettedPS[0] == "!hand" or targettedPS[0] == "!pass" or targettedPS[0] == "!lob" or targettedPS[0] == "!chuck" or targettedPS[0] == "!toss" or targettedPS[0] == "!punt" or targettedPS[0] == "!pitch" or targettedPS[0] == "!fling" or targettedPS[0] == "!hurl"):
				self.callResponseScript("lg",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "kick"):
				self.callResponseScript("kick",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "rankick"):
				self.callResponseScript("rankick",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "shutup" or targettedPS[0] == "shup"):
				self.callResponseScript("shup",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "unshutup" or targettedPS[0] == "unshup"):
				self.callResponseScript("shup",command,isDescription,user,channel,{"unshup":1});
			elif (targettedPS[0] == "whois"):
				self.callResponseScript("account_misc",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "whoami"):
				self.callResponseScript("account_misc",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "editprofile"):
				self.callResponseScript("account_misc",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "accounthelp"):
				self.callResponseScript("account_misc",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "managehosts"):
				self.callResponseScript("account_misc",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "changepassword"):
				self.callResponseScript("account_misc",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "login"):
				self.callResponseScript("account_login",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "logout"):
				self.callResponseScript("account_login",command,isDescription,user,channel,{"logout":1});
			elif (targettedPS[0] == "createaccount"):
				self.callResponseScript("account_create",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "stealth"):
				self.callResponseScript("stealth",command,isDescription,user,channel,{});
			#elif (targettedPS[0] == "suggest"):
			#	self.callResponseScript("content",command,isDescription,user,channel,{});
			elif (targettedPS[0] == "is"):
				self.connection.sendMsg( self.getRecipient(user,channel),self.fileSystem.getRandomLine(os.path.join("misc","is.txt"),1));
			elif (targettedPS[0] == "commands" or targettedPS[0] == "help"):
				self.connection.sendMsg( self.getRecipient(user,channel),"http://platopus.senselesspoliticalramblings.com/commands.html");
		else:
			newCommand = "";
			if (channel != ""):
				if (len(self.channelEncoreHistory[channel.lower()]) > 0):
					#print "found channel line";
					newCommand = self.channelEncoreHistory[channel.lower()][len(self.channelEncoreHistory[channel.lower()])-1];
			if (newCommand == ""):
				if (user != None and len(user.encoreHistory) > 0):
					#print "found user line";
					newCommand = user.encoreHistory[len(user.encoreHistory)-1];
			if (newCommand == ""):
				if (len(self.globalEncoreHistory) > 0):
					#print "found global line";
					newCommand = self.globalEncoreHistory[len(self.globalEncoreHistory)-1];
			if (newCommand != ""):
				#print "using: "+newCommand;
				self.callResponse(newCommand,isDescription,user,channel);
			else:
				self.connection.sendMsg( self.getRecipient(user,channel), "I haven't done anything to encore yet.");
	else:
		# UNRECOGNIZED COMMAND
		UNRECOGNIZED_COMMAND_MSG = "Unrecognized command. For a complete command list, see: http://platopus.senselesspoliticalramblings.com/commands.html";
		if (channel == ""):
			# query... so send it back
			self.connection.sendMsg(user.nick,UNRECOGNIZED_COMMAND_MSG);
		else:
			# channel... so notice it
			self.connection.sendNotice(user.nick,UNRECOGNIZED_COMMAND_MSG);
