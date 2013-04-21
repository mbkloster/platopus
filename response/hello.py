# standard greeting response script
# This is NOT meant to be executed by itself, but
# rather, as part of ResponseSystem.

self.connection.sendMsg(self.getRecipient(user,channel),self.parse(self.fileSystem.getRandomLine(os.path.join(".","misc","hello.txt")),"",user,channel) );