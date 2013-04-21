# platopus LIVE GRENADE script
# this script handles all lg-related stuff... tossing, fumbles etc.

from time import time;
from threading import Timer;

command = command.split(" ");

MIN_ACTIVITY_MINS = 7;
GAME_TIMEOUT_MINS = 3;
PASS_PENALTY_SECS = -2; # fumble penalty
BAD_PASS_PENALTY_SECS = -1; # bad pass penalty
MIN_TIME_REMAINING_SECS = 0.005;

print "Hi :) I'm starting here";

POSSIBLE_ACTIONS = [
["hand",[0.98,0.02,0.00],3,"{t1} takes the grenade and graciously hands it to {t2}."],
["pass",[0.90,0.00,0.10],2,"{t1} makes a pass with the grenade to {t2}!"],
["lob",[0.88,0.06,0.06],1,"{t1} lifts the grenade up and lobs it over to {t2}!"],
["chuck",[0.82,0.04,0.14],-1,"{t1} nervously chucks the grenade to {t2}."],
["toss",[0.82,0.09,0.09],0,"{t1} grabs the grenade and tosses it to {t2}!"],
["punt",[0.72,0.13,0.17],-1,"{t1} punts the grenade to {t2} aggressively."],
["pitch",[0.68,0.16,0.16],-1,"{t1} pauses momentarily and pitches the grenade right at {t2}!"],
["fling",[0.62,0.28,0.10],-2,"{t1} quickly flings the grenade at surprised {t2}!"],
["hurl",[0.50,0.35,0.15],-3,"{t1} HURLS the grenade at {t2}, who barely manages to catch it!"],
];

def killTarget(self, target, channel):
	global GAME_TIMEOUT_MINS, time;
	if (target.nick.lower() != self.console.getVar("lg_server").lower()):
		server = self.connection.getUser(self.console.getVar("lg_server"));
		server.addPoints(7);
		message = self.fileSystem.getRandomLine(os.path.join("rsg","wordbank","exclamations.txt")).capitalize()+", that was "+self.fileSystem.getRandomLine(os.path.join("rsg","wordbank","adjectives.txt")).split("|")[0]+"! "+self.console.getVar("lg_server")+" made the killing shot for +7 points. Live Grenade will now be deactivated for "+str(GAME_TIMEOUT_MINS)+" minutes. Thank you for playing!";
	else:
		message = self.fileSystem.getRandomLine(os.path.join("rsg","wordbank","exclamations.txt")).capitalize()+", that wasn't very "+self.fileSystem.getRandomLine(os.path.join("rsg","wordbank","adjectives.txt")).split("|")[0]+"! "+self.console.getVar("lg_server")+" committed suicide, and I can't condone that, so no points. Live Grenade will now be deactivated for "+str(GAME_TIMEOUT_MINS)+" minutes. Thank you for playing!";
	if (random.random() <= 0.40):
		self.connection.sendMsg(channel,"The LIVE GRENADE just "+self.fileSystem.getRandomLine(os.path.join("rsg","wordbank","verbs.txt")).split("|")[2].upper()+" in "+target.nick+"'s FACE!");
	else:
		self.connection.sendMsg(channel,"The LIVE GRENADE just BLEW UP in "+target.nick+"'s FACE!");
	self.connection.kickUser(channel,target.nick,"BOOM");
	self.connection.sendMsg(channel,message);
	self.console.setVar("lg_target","");
	self.console.setVar("lg_target_history","");
	self.console.setVar("lg_last_pass",0);
	self.console.setVar("lg_last_time",0);
	self.console.setVar("lg_server","");
	self.console.setVar("lg_channel","");
	self.console.setVar("lg_fumble_action","");
	self.console.setVar("lg_fumble_target","");
	self.console.setVar("lg_last_game",time());

def notifyTarget(self, target, channel):
	self.connection.sendMsg(channel,""+target.nick+": You have3 "+str(int(self.console.getVar("lg_last_time")))+" seconds to pass the grenade! Use either !4"+self.console.getVar("lg_action1")+" [nick] or !4"+self.console.getVar("lg_action2")+" [nick] to pass.");

def setActions(self):
	global POSSIBLE_ACTIONS;
	if (random.random() <= 0.15):
		action1 = 0;
	else:
		action1 = self.console.random.randInt(0,len(POSSIBLE_ACTIONS)-1);
	action2 = -1;
	while (action2 == -1 or action2 == action1):
		action2 = self.console.random.randInt(0,len(POSSIBLE_ACTIONS)-1);
	self.console.setVar("lg_action1",POSSIBLE_ACTIONS[action1][0]);
	self.console.setVar("lg_action2",POSSIBLE_ACTIONS[action2][0]);

if (channel != ""):
	if (command[0].lower() == "lg" and self.console.getVar("lg_target") == ""):
		if ((user.loginUserLevel >= 2 or self.checkPointRequirement(user,channel,5,"start a game of Live Grenade")) and time() >= self.console.getVar("lg_last_game")+GAME_TIMEOUT_MINS*60):
			userList = self.connection.channels[channel.lower()];
			selectableUsers = [];
			reportedError = 0;
			for currentUser in userList:
				if (currentUser.nick.lower() != self.connection.currentNick.lower() and currentUser.nick.lower() != "monobot" and currentUser.nick.lower() != "q" and currentUser.nick.lower() != "duckbread" and currentUser.lastPublicMsg >= time()-MIN_ACTIVITY_MINS*60 and selectableUsers.count(currentUser) <= 0):
					selectableUsers.append(currentUser);
			if (len(command) > 1):
				# a target has already been specified
				if (command[1].lower() == self.connection.currentNick.lower() or command[1].lower() == "duckbread" or command[1].lower() == "q" or command[1].lower() == "monobot" or command[1].lower() == "me"):
					target = self.isInChannel(user.nick,channel);
				else:
					target = self.isInChannel(command[1],channel);
				
				if (target == None):
					self.connection.sendMsg(self.getRecipient(user,channel),""+command[1]+" does not seem to be in "+channel+".");
					reportedError = 1;
				
			else:
				# pick a target randomly
				if (len(selectableUsers) >= 2):
					target = selectableUsers[self.console.random.randInt(0,len(selectableUsers)-1)];
			
			if (len(selectableUsers) < 2 and not reportedError):
				target = None;
				self.connection.sendMsg(channel,"Sorry, bro, not enough people around to play Live Grenade. You need at least 2 active non-bot users in the last "+str(MIN_ACTIVITY_MINS)+" minutes.");
			else:
				print "ffffffffff:";
				for xxx in selectableUsers:
					print xxx.nick;
			
			if (target != None and target.lastPublicMsg < time()-MIN_ACTIVITY_MINS*60):
				self.connection.sendMsg(self.getRecipient(user,channel),""+target.nick+" is either a bot or has not done anything in the last "+str(MIN_ACTIVITY_MINS)+" minutes and cannot handle the Live Grenade.");
				target = None;
			elif (target != None):
				initialTime = self.console.random.randInt(16,24);
				self.console.setVar("lg_target",target.nick);
				self.console.setVar("lg_target_history"," "+target.nick.lower()+" ");
				self.console.setVar("lg_last_pass",time());
				self.console.setVar("lg_last_time",initialTime);
				self.console.setVar("lg_server",user.nick);
				self.console.setVar("lg_channel",channel);
				self.console.setVar("lg_fumble_action","");
				self.console.setVar("lg_fumble_target","");
				if (target.nick == user.nick):
					self.connection.sendMsg(self.getRecipient(user,channel),""+target.nick+" pulls out the LIVE GRENADE, eyeing possible victims to toss it to. ("+str(initialTime)+"s)");
				else:
					self.connection.sendMsg(self.getRecipient(user,channel),""+user.nick+" pulls out the LIVE GRENADE and hands it to "+target.nick+"! ("+str(initialTime)+"s)");
				setActions(self);
				notifyTarget(self,target,channel);
				self.console.threads["lg_kill"] = Timer(initialTime,killTarget,args=(self,target,channel));
				self.console.threads["lg_kill"].start();
		elif (time() < self.console.getVar("lg_last_game")+GAME_TIMEOUT_MINS*60):
			print "time";
			self.connection.sendMsg(self.getRecipient(user,channel),"Sorry, but you must wait at least "+str(GAME_TIMEOUT_MINS)+" minutes between games of LIVE GRENADE. Thank you for your patience.");
		else:
			print "something else";
	elif (len(command) >= 2 and command[0].lower() == "lg" and command[1].lower() == "off"):
		if (self.isOpInChannel(user.nick,channel)):
			self.console.setVar("lg_target","");
			self.console.setVar("lg_target_history","");
			self.console.setVar("lg_last_pass",0);
			self.console.setVar("lg_last_time",0);
			self.console.setVar("lg_server","");
			self.console.setVar("lg_channel","");
			self.console.setVar("lg_fumble_action","");
			self.console.setVar("lg_fumble_target","");
			self.console.setVar("lg_last_game",time());
			if (self.console.hasThread("lg_kill")):
				self.console.threads["lg_kill"].cancel();
			self.connection.sendMsg(self.getRecipient(user,channel),"The LIVE GRENADE has been safely deactivated. No one has been harmed. The game will now be deactivated for "+str(GAME_TIMEOUT_MINS)+" minutes. Thank you!");
		else:
			self.connection.sendMsg(self.getRecipient(user,channel),"You must be an op to use this command.");
	elif (command[0].lower() == "redirect"): # redirecting stuff
		if (self.console.getVar("lg_target") != ""):
			if (user.channels.has_key(channel.lower()) and user.channels[channel.lower()]):
				if (len(command) > 1):
					if (command[1].lower() == "me"):
						command[1] = user.nick;
					target = self.isInChannel(command[1],channel);
					if (target != None and self.console.getVar("lg_last_pass")-time()+self.console.getVar("lg_last_time") > MIN_TIME_REMAINING_SECS):
						if (target.nick.lower() == self.connection.currentNick.lower() or target.nick.lower() == "q" or target.nick.lower() == "monobot" or target.nick.lower() == "duckbread"):
							target = user;
						self.console.setVar("lg_target",target.nick);
						self.console.setVar("lg_target_history",self.console.getVar("lg_target_history")+" "+target.nick.lower()+" ");
						self.console.setVar("lg_last_pass",time());
						self.console.setVar("lg_server",user.nick);
						self.console.setVar("lg_channel",channel);
						self.console.setVar("lg_fumble_action","");
						self.console.setVar("lg_fumble_target","");
						if (self.console.hasThread("lg_kill")):
							self.console.threads["lg_kill"].cancel();
						self.console.threads["lg_kill"] = Timer(self.console.getVar("lg_last_time"),killTarget,args=(self,target,channel));
						self.console.threads["lg_kill"].start();
						self.connection.sendMsg(self.getRecipient(user,channel),""+user.nick+" magically redirects the grenade to "+target.nick+"!");
						setActions(self);
						notifyTarget(self,target,channel);
					elif (target == None):
						self.connection.sendMsg(self.getRecipient(user,channel),"I can't seem to find "+command[1]+" on "+channel+".");
			else:
				self.connection.sendMsg(self.getRecipient(user,channel),"Only ops may redirect the grenade.");
		else:
			self.connection.sendMsg(self.getRecipient(user,channel),"This command may only be used when there is an active game of Live Grenade.");
			
	else: # some other command other than starting lg
		print "Yo gatorade me bitch";
		if (self.console.getVar("lg_target") != "" and self.console.getVar("lg_target").lower() == user.nick.lower()):
			print "Sup";
			if (len(command) >= 2 and (command[0].lower() == self.console.getVar("lg_action1") or command[0].lower() == self.console.getVar("lg_action2") or command[0].lower() == "!"+self.console.getVar("lg_action1") or command[0].lower() == "!"+self.console.getVar("lg_action2"))):
				print "arg barg";
				action = None;
				for action in POSSIBLE_ACTIONS:
					print str(action)+" DAAAAAAAAAA "+str(command[0]);
					if (action[0] == command[0].lower()):
						break;
					elif ("!"+action[0] == command[0].lower() ):
						break;
				userList = self.connection.channels[channel.lower()];
				selectableUsers = [];
				reportedError = 0;
				for currentUser in userList:
					if (currentUser.nick.lower() != self.connection.currentNick.lower() and currentUser.nick.lower() != "monobot" and currentUser.nick.lower() != "q" and currentUser.nick.lower() != "duckbread" and currentUser.lastPublicMsg >= time()-MIN_ACTIVITY_MINS*60 and selectableUsers.count(currentUser) <= 0):
						selectableUsers.append(currentUser);
				passSuccessful = 1;
				target = self.isInChannel(command[1],channel);
				if (target == None):
					self.connection.sendMsg(self.getRecipient(user,channel),"I can't seem to find "+command[1]+" on "+channel+".");
					passSuccessful = 0;
				elif (target.nick.lower() == user.nick.lower()):
					self.connection.sendMsg(self.getRecipient(user,channel),"You cannot pass the grenade to yourself.");
					passSuccessful = 0;
				elif (target.nick.lower() == "q" or target.nick.lower() == "monobot" or target.nick.lower() == "duckbread" or target.nick.lower() == self.connection.currentNick.lower()):
					self.connection.sendMsg(self.getRecipient(user,channel),""+user.nick+" is an idiot! (4"+str(BAD_PASS_PENALTY_SECS)+"s)");
					totalDeltaTime = self.console.getVar("lg_last_pass")-time()+BAD_PASS_PENALTY_SECS;
					newTime = self.console.getVar("lg_last_time")+totalDeltaTime;
					self.console.setVar("lg_last_pass",time());
					self.console.setVar("lg_last_time",newTime);
					if (self.console.hasThread("lg_kill")):
						self.console.threads["lg_kill"].cancel();
					self.console.threads["lg_kill"] = Timer(newTime,killTarget,args=(self,user,channel));
					self.console.threads["lg_kill"].start();
					passSuccessful = 0;
				elif (selectableUsers.count(target) <= 0):
					self.connection.sendMsg(self.getRecipient(user,channel),""+target.nick+" has not said anything in the past "+str(MIN_ACTIVITY_MINS)+" minutes and cannot be passed to.");
					passSuccessful = 0;
				elif (target.nick.lower() == self.console.getVar("lg_fumble_target") and command[0].lower() == self.console.getVar("lg_fumble_action")):
					self.connection.sendMsg(channel,""+user.nick+": You must change up either your action or target after you fumble.");
					passSuccessful = 0;
				elif (self.console.getVar("lg_last_pass")-time()+self.console.getVar("lg_last_time") <= MIN_TIME_REMAINING_SECS):
					passSuccessful = 0;
				
				if (passSuccessful): # now, test for fumbles/spinouts
					passOutcome = getOutcome(action[1]);
					print str(passOutcome)+" came of it";
					if (passOutcome == 1): # FUMBLE!
						self.connection.sendMsg(channel,""+user.nick+" fumbles and must pass differently! (4"+str(PASS_PENALTY_SECS)+"s/-2pts)")
						if (command[0] == self.console.getVar("lg_action1")):
							self.connection.sendMsg(channel,""+user.nick+": You must now either 4"+self.console.getVar("lg_action2")+" [target] or 4"+self.console.getVar("lg_action1")+" [someone else]");
						else:
							self.connection.sendMsg(channel,""+user.nick+": You must now either !4"+self.console.getVar("lg_action1")+" [target] or !4"+self.console.getVar("lg_action2")+" [someone else]");
						user.deductPoints(2);
						totalDeltaTime = self.console.getVar("lg_last_pass")-time()+PASS_PENALTY_SECS;
						newTime = self.console.getVar("lg_last_time")+totalDeltaTime;
						self.console.setVar("lg_last_pass",time());
						self.console.setVar("lg_last_time",newTime);
						self.console.setVar("lg_fumble_action",command[0].lower());
						self.console.setVar("lg_fumble_target",target.nick.lower());
						if (self.console.hasThread("lg_kill")):
							self.console.threads["lg_kill"].cancel();
						self.console.threads["lg_kill"] = Timer(newTime,killTarget,args=(self,user,channel));
						self.console.threads["lg_kill"].start();
						passSuccessful = 0;
					elif (passOutcome == 2): # MISS!
						targetHistory = self.console.getVar("lg_target_history");
						if (selectableUsers.count(user)):
							selectableUsers.remove(user);
						targetHistory = targetHistory.replace(" "+user.nick.lower()+" ","");
						if (selectableUsers.count(target)):
							selectableUsers.remove(target);
						targetHistory = targetHistory.replace(" "+target.nick.lower()+" ","");
						if (len(selectableUsers) > 0):
							# miss successful
							newTarget = selectableUsers[self.console.random.randInt(0,len(selectableUsers)-1)];
							while (targetHistory.find(" "+newTarget.nick.lower()+" ") < 0):
								newTarget = selectableUsers[self.console.random.randInt(0,len(selectableUsers)-1)];
							self.connection.sendMsg(channel,""+user.nick+" takes the grenade, attempts to toss... and misses! It ends up in "+newTarget.nick+"'s hands!");
							self.console.setVar("lg_target",newTarget.nick);
							self.console.setVar("lg_target_history",self.console.getVar("lg_target_history")+" "+newTarget.nick.lower()+" ");
							self.console.setVar("lg_last_pass",time());
							self.console.setVar("lg_server",user.nick);
							setActions(self);
							notifyTarget(self,newTarget,channel);
							if (self.console.hasThread("lg_kill")):
								self.console.threads["lg_kill"].cancel();
							self.console.threads["lg_kill"] = Timer(self.console.getVar("lg_last_time"),killTarget,args=(self,newTarget,channel));
							self.console.threads["lg_kill"].start();
							passSuccessful = 0;
						else:
							# treat it as a fumble...
							self.connection.sendMsg(channel,""+user.nick+" fumbles and must pass differently! (4"+str(PASS_PENALTY_SECS)+"s/-2pts)")
							if (command[0] == self.console.getVar("lg_action1")):
								self.connection.sendMsg(channel,""+user.nick+": You must now either !4"+self.console.getVar("lg_action2")+" [any user] or !4"+self.console.getVar("lg_action1")+" [someone else]");
							else:
								self.connection.sendMsg(channel,""+user.nick+": You must now either !4"+self.console.getVar("lg_action1")+" [any user] or !4"+self.console.getVar("lg_action2")+" [someone else]");
							user.deductPoints(2);
							totalDeltaTime = self.console.getVar("lg_last_pass")-time()+PASS_PENALTY_SECS;
							newTime = self.console.getVar("lg_last_time")+totalDeltaTime;
							self.console.setVar("lg_last_pass",time());
							self.console.setVar("lg_last_time",newTime);
							self.console.setVar("lg_fumble_action",command[0].lower());
							self.console.setVar("lg_fumble_target",target.nick.lower());
							if (self.console.hasThread("lg_kill")):
								self.console.threads["lg_kill"].cancel();
							self.console.threads["lg_kill"] = Timer(newTime,killTarget,args=(self,user,channel));
							self.console.threads["lg_kill"].start();
							passSuccessful = 0;
				if (passSuccessful): # now, try to actually pass the grenade
					if (time()-self.console.getVar("lg_last_pass") < 5):
						pointsGiven = 4;
					else:
						pointsGiven = 2;
					user.addPoints(pointsGiven);
					totalDeltaTime = (self.console.getVar("lg_last_pass")-time())/2+action[2];
					newTime = self.console.getVar("lg_last_time")+totalDeltaTime;
					if (newTime < 3):
						newTime = 3;
					self.console.setVar("lg_target",target.nick);
					self.console.setVar("lg_target_history",self.console.getVar("lg_target_history")+" "+target.nick.lower()+" ");
					self.console.setVar("lg_last_pass",time());
					self.console.setVar("lg_last_time",newTime);
					self.console.setVar("lg_server",user.nick);
					self.console.setVar("lg_channel",channel);
					self.console.setVar("lg_fumble_action","");
					self.console.setVar("lg_fumble_target","");
					message = action[3].replace("{t1}",""+user.nick+"").replace("{t2}",""+target.nick+"");
					if (action[2] < 0):
						self.connection.sendMsg(self.getRecipient(user,channel),message+" (4"+str(action[2])+"s/+"+str(pointsGiven)+"pts)");
					else:
						self.connection.sendMsg(self.getRecipient(user,channel),message+" (9+"+str(action[2])+"s/+"+str(pointsGiven)+"pts)");
					
					if (self.console.hasThread("lg_kill")):
						self.console.threads["lg_kill"].cancel();
					
					setActions(self);
					notifyTarget(self,target,channel);
					self.console.threads["lg_kill"] = Timer(newTime,killTarget,args=(self,target,channel));
					self.console.threads["lg_kill"].start();
				
			else:
				self.connection.sendMsg(channel,""+user.nick+": You must either "+self.console.getVar("lg_action1")+" or "+self.console.getVar("lg_action2")+" the grenade, and specify a target.");
		elif (self.console.getVar("lg_target") == ""):
			self.connection.sendMsg(channel,"A Live Grenade game must be enabled to use this command. Use the 'lg' command to enable Live Grenade.");
		elif (self.console.getVar("lg_target").lower() == user.nick.lower()):
			self.connection.sendNotice(target.nick,"You do not currently hold the grenade.");
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"You can only use this command in a channel.");