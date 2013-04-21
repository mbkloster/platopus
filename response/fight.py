#platopus FIGHT script!!!

def fac(n):
	result = 1;
	for i in range(1,n+1):
		result *= i;
	return result;

def getValue(target):
	global fac;
	# gets the numerical value of a target
	if (target != "platopus"):
		value = 0;
		previousC = 0;
		for c in target:
			C = ord(c);
			difference = abs(C-previousC);
			value += (difference + C*previousC + fac(C%8))%17;
			value += (ord(c) % 6);
			previousC = C;
		value -= len(target)*2/3;
		#if (value < 0):
		#	value *= -1;
		value %= 185;
		value += 15;
		if (target == "fun"):
			value += 10;
	else:
		value = 999999999;
	return value;

def getWeapon(target):
	# gets the weapon id of a target
	if (target != "platopus"):
		return (ord(target[0:1]) + ord(target[-1:]) + len(target)) % 7;
	else:
		return 7;

command = command.split(" ");
if (len(command) >= 3):
	weapons = (
	("a flamethrower","{t1} barely manages to roast {t2} with a flamethrower.","{t1} roasts {t2} to a flaming crisp with the help of some kerosene.","{t1} reduces {t2} to a crispy, roasted bunch of flesh and bones."),
	("bare fists","{t1} manages to get a lucky punch on {t2}, delivering a knockout. Barely.","{t1} punches {t2} right in the goddamn face.","{t1} repeatedly punches {t2} into a worthless pulp."),
	("a gigantic longsword","{t1} manages to barely get {t2} with a longsword.","{t1} strikes {t2} down with a longsword.","{t1} hacks {t2} to pieces with a huge longsword."),
	("a sledgehammer","{t1} manages to distract {t2}, sneaking in a barely-successful hit with a sledgehammer.","{t1} takes a sledgehammer and clobbers {t2} in the face with it.","{t1} turns {t2} into a bloody sledgehammered mess."),
	("a deep dark curse","After almost facing a brutal beatdown, {t1} learns shamanism and manages, with some effort, to turn {t2} into a frog.","{t1}, knowing the art of shamanism, gives {t2} herpes.","Without even thinking about it, {t1} turns {t2} into a tiny ant, conveniently squishable."),
	("rockets","Apparently barely knowing how to use a rocket launcher, {t1} gets lucky and blows away {t2} by the feet.","{t1} victimizes {t2} with a precise rocket to the chest.","{t1} takes aim and blows away {t2} with an easily-timed rocket, then smokes to celebrate."),
	("a toilet","{t1} uses the old \"look over there\" trick and clobbers {t2} with the help of a toilet during the momentary distraction.","{t1} manages to smack {t2} across the head with a toilet.","{t1} chucks a toilet at {t2}, resulting in a dead {t2} and a bloody toilet."),
	("the unholy power of his mind","{t1} barely mind flays {t2}","{t1} mind flays {t2}","All it took was a simple glance from {t1} into the eyes of {t2} to cause immediate, painful death."));
	targets = command[1:];
	if (targets > 5):
		targets = targets[0:5];
	targets2 = []; # an exact copy of the targets, with no duplicates
	targetValues = [];
	baseTarget = targets[0].lower();
	for target in targets:
		existsAlready = 0;
		for target2 in targets2:
			if (target2.lower() == target.lower()):
				existsAlready = 1;
				break;
		if (not existsAlready):
			targets2.append(target);
	
	# now sort the targets
	for i in range(0,len(targets2)):
		targets2[i] = targets2[i].replace("_"," ");
		targets2[i] = (getValue(targets2[i].lower()),targets2[i]);
	targets2.sort();
	targets2.reverse();
	message = "";
	
	if (len(targets2) > 1):
		if (len(targets2) == 2):
			margin = targets2[0][0]-targets2[1][0];
			if (margin > 0):
				if (margin < 4):
					message = weapons[getWeapon(targets2[0][1].lower())][1];
				elif (margin < 20):
					message = weapons[getWeapon(targets2[0][1].lower())][2];
				else:
					message = weapons[getWeapon(targets2[0][1].lower())][3];
			else:
				message = "After a brutal, epic, cinematic battle on a very high production budget, {t1} and {t2} tie. What a cocktease.";
			message = message.replace("{t1}",""+targets2[0][1]+" ("+str(targets2[0][0])+")");
			message = message.replace("{t2}",""+targets2[1][1]+" ("+str(targets2[1][0])+")");
		else:
			message += ""+targets2[0][1]+" ("+str(targets2[0][0])+") beats ";
			for i in range(1,len(targets)):
				message += ""+targets2[i][1]+" ("+str(targets2[i][0])+") ";
			message += "with "+weapons[getWeapon(targets2[0][1].lower())][0]+".";
	else:
		message = ""+targets2[0][1]+" ("+str(targets2[0][0])+") realizes that life is merely an extended conflict between the many facets of one's self, and that \"winning\" and \"losing\" merely represent one's degree of success in overcoming these conflicts.";
	self.connection.sendMsg(self.getRecipient(user,channel),message);
else:
	self.connection.sendMsg(self.getRecipient(user,channel),"Usage: fight [combatant 1] [combatant 2] [combatant 3]....");