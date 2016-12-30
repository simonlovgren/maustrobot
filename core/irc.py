import socket, re, time
import core.msgparser as msgparser
import importlib

class IRC:
    # Settings
    sleepTime = 1
    tagsEnabled = 1
    lastrun = 0;

    # Globals
    config = []
    chat = None

    def __init__(self, conf):
        self.config = conf

    def stopped(self):
        self.killed = True
        print("Stopped bot (#%s)" % self.config["channel"])

    def send(self, msg):
        print("")
        print("-------- SENDING --------")
        print(msg)
        self.chat.send(msg.encode("utf-8"))

    def receive(self):
        return self.chat.recv(1024).decode("utf-8")

    def say(self, message):
        self.send("PRIVMSG #%s :%s\r\n" % (self.config["channel"], message))

    def whisper(self, user, message):
        self.say("/w %s %s" % (user, message))

    def connect(self):
        # Create socket and connect to server
        self.chat = socket.socket()
        #self.chat.settimeout(0.5)
        self.chat.connect((self.config["host"], int(self.config["port"])))
        # Log in to server
        self.send("PASS oauth:%s\r\n" % (self.config["password"]))
        self.send("NICK %s\r\n" % (self.config["nick"]))
        # Join channel
        self.send("JOIN #%s\r\n" % (self.config["channel"]))
        # Request tags
        if self.tagsEnabled:
            self.send("CAP REQ :twitch.tv/tags\r\n")
        # Request commands
        self.send("CAP REQ :twitch.tv/commands\r\n")
        # Request membership state event messages
        self.send("CAP REQ :twitch.tv/membership\r\n")

        # Wait and detect when fully connected
        connected = 0
        while not connected:
            message = self.receive()
            print(message)
            message = msgparser.parseMessage(message)
            for msg in message:
                print(msg)
                # If we see the end of the names list
                # we've successfully connected to the
                # server and are ready to continue
                if msg["type"] == "server" and msg["code"] == "366":
                    connected = 1

        print("Connected to %s" % (self.config["channel"]))

    def disconnect(self):
        # Part from channel
        self.send("PART #%s\r\n" % (self.config["channel"]))
        self.chat.close()

    def parseMessage(self, msg):
        # Parse tags if present
        if self.tagsEnabled:
            pass

    def commands(self, msg):
        pass
                
    def filters(self, msg):
        pass

    def listen(self):
        try:
            while 1:
                # Grab message
                message = self.receive()
                # Print message
                print("")
                print("-------- RECEIVING --------")
                print(message)
                #check for twitch ping and pong it back
                # otherwise we'll be dropped from chat
                if message == "PING :tmi.twitch.tv\r\n":
                    self.send("PONG :tmi.twitch.tv\r\n")
                else:
                        for msg in msgparser.parseMessage(message):
                                if msg['type'] == 'message' and msg['message'][0] == "!":
                                        print("Command")
                                        # Check that we aren't spamming the chat
                                        timestamp = int(time.time())
                                        if (self.lastrun + self.sleepTime) > timestamp:
                                                time.sleep(self.lastrun + self.sleepTime - timestamp);  # If delay not passed, wait remaining time
                                        # Run commands
                                        self.commands(msg)
                                        # Run filter actions
                                        #self.filters(msg)
                                        lastrun = int(time.time())

                                        # Delay to free up resources
                                        time.sleep(0.01)

        except KeyboardInterrupt:
            self.disconnect()
            self.stopped()

    def start(self):
        self.connect()
        self.listen()
