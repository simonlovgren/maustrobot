import socket, re
from time import sleep


class Bot:
	# Settings
	sleepTime = 1

	# Globals
	config = []
	chat = None

	def __init__(self, conf):
		self.config = conf

	def stopped(self):
		self.killed = True
		print("Stopped bot (%s)" % self.config["channel"])

	def send(self, msg):
		print("")
		print("-------- SENDING --------")
		print(msg)
		self.chat.send(msg.encode("utf-8"))

	def say(self, message):
		self.send("PRIVMSG %s :%s\r\n" % (self.config["channel"], message))

	def whisper(self, user, message):
		self.say("/w %s %s" % (user, message))

	def connect(self):
		# Create socket and connect to server
		self.chat = socket.socket()
		#self.chat.settimeout(0.5)
		self.chat.connect((self.config["host"], int(self.config["port"])))
		# Log in to server
		self.send("PASS %s\r\n" % (self.config["password"]))
		self.send("NICK %s\r\n" % (self.config["nick"]))
		# Join channel
		self.send("JOIN %s\r\n" % (self.config["channel"]))
		# Request tags
		self.send("CAP REQ :twitch.tv/tags\r\n")
		# Request commands
		self.send("CAP REQ :twitch.tv/commands\r\n")
		# Request JOIN/PART messages
		self.send("CAP REQ :twitch.tv/membership\r\n")

	def disconnect(self):
		self.chat.close()

	def filters(self, msg):
		pass

	def listen(self):
		try:
			while 1:
				# Grab message
				message = self.chat.recv(1024).decode("utf-8")
				# Print message
				print("")
				print("-------- RECEIVING --------")
				print(message)
				#check for twitch ping and pong it back
				# otherwise we'll be dropped from chat
				if message == "PING :tmi.twitch.tv\r\n":
					self.send("PONG :tmi.twitch.tv\r\n")
				else:
					# Run filter actions
					self.filters(message)

				# Delay to free up resources
				sleep(0.01)

		except KeyboardInterrupt:
			self.disconnect()
			self.stopped()

	def start(self):
		self.connect()
		self.listen()
