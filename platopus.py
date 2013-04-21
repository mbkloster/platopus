########################################
# platopus main script
########################################
#
# This pretty much launches everything else.
# Password for Q: aA89.X3F_ffg1
#

##############################
# END PLATOPUS SETTINGS
##############################

# Product name
PRODUCT_NAME = "platopus";
# Product version
PRODUCT_VERSION = "1.01";

from Connection import Connection;
from Console import Console;
from time import time, sleep;
from threading import Thread, Timer;
from Settings import Settings;
import random;

print "Welcome to "+PRODUCT_NAME+" (version "+PRODUCT_VERSION+")";
print "Written and created by Matthew Kloster";
print "Command console ready. Send commands to cmd.txt.\n";

random.seed(time());

console = Console(PRODUCT_NAME+".log");
console.adjustDate(time());
console.sessionStart(time());

if (Settings.AUTO_CONNECT):
	console.createConnection();
	console.threads["connect"] = Thread(target=console.connection.IRCConnect);
	console.threads["connect"].setDaemon(1);
	console.threads["connect"].start();

while (console.active):
	fp = open("cmd.txt","r");
	command = fp.read();
	fp.close();
	command = command.replace("\n","");
	if (command != ""):
		console.send(command);
		fp = open("cmd.txt","w");
		fp.write("");
		fp.close();
	sleep(0.5);
