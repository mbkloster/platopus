# platopus

## Background

Around 2009, there was a need for a replacement "entertainment" IRC bot after Tickbot, the one previously used, went into an indefinite hiatus. Tickbot was written in mircscript, and while I could've worked out a way to get it imported and working on my own machine, I decided it would be better to write my own from scratch in Python.

I decided not to use any external libraries or interfaces to work on the IRC portion of things. I'd already had quite a bit of familiarity with the IRC protocol, so extending my knowledge to another project wasn't such a big deal, and it would allow me a lot more control over how this was done.

As such, this bot should more or less work 100% out of the box, with no external library installations necessary. It's designed for Python 2.x, but if you wanted to you could use 2to3 to bring it up to the latest Python version - see http://docs.python.org/dev/howto/pyporting.html
It's also designed to connect to quakenet by default, and some channels that you'll probably want to change. You can fix these settings up by taking a quick jump into Settings.py.

## What's There, What's Not

For those that have used platopus before, this is a pretty complete set of features, minus user accounts and data files. This includes:

- A searchable quote function.
- The LIVE GRENADE game (an interesting IRC-based version of hot potato)
- "Who would win" style fight game that determines winners based on names only

However, just because some of these algorithms were interesting enough for me to ponder later use of them, I decided not to include "jabber" (random sentense mashups with some intelligent joining) or "rsg" (the random sentence generator) scripts on here. They may come at a later time.

## How to Use

As mentioned before, this script works pretty much straight out of the box by running platopus.py. You'll need to feed commands to by piping lines of commands in to cmd.txt, which will automatically pick them up and process them. You can get a list of commands from combing through Console.py.

"Response scripts" (the kind that determine how the bot reacts to certain commands) are stored in the responses/ directory. When you make a change to one of them, say test.py, you don't need to reboot the bot to see that change take effect. Instead, just run the command "reloadresponse test". They way that commands are directed into responses is determined by ResponseIndex.py, which can also be reloaded mid-flight via the command "reloadresponseindex". You'll NEED to run these commands to see your changes take effect! Note that if a command has never been used by the bot, its accompanying response script will not be loaded into memory yet.
