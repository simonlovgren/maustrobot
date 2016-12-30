#!/usr/bin/env python3
import configparser
from core.irc import IRC

# Config handle
config = configparser.ConfigParser()
bot = None

## Initialize bots
def init():
	global config, bot

	# Get config
	config.read("bot.conf")
	config = config["DEFAULT"]

	# Create and start bot
	irc = IRC(config)
	irc.start()

if __name__ == "__main__":
	init()
