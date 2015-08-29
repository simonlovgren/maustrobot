#!/usr/bin/python
import random, binascii

def loadMessages():
	count = 0
	lines = []
	with open("ping.conf") as f:
		for line in f:
			# Clean up trailing and leading whitespaces
			# as well as newlines and tabs
			line = line.strip(' \t\n\r')
			# Filter comments
			if not line or line[0] == "#":
				continue
			lines.append(line)
			count = count + 1

	return lines, count

def selectMessage(count, messages):
	return messages[random.randint(0,count-1)]

def ping(bot):
	# Grab available messages
	messages, count = loadMessages()
	# Select random message
	message = selectMessage(count, messages)
	# Convert to HEX with space every 2 chars
	message = binascii.hexlify(message.encode("ascii")).decode("ascii").upper()
	i = iter(message)								# iterator
	message = " ".join(a+b for a,b in zip(i,i))		# create pairs of 2 and join on space

	# Print message
	bot.say(message)								# Make bot write message to chat


if __name__ == "__main__":
	ping()