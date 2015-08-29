import configparser
from core.bot import Bot 

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
	bot = Bot(config)
	bot.start()

if __name__ == "__main__":
	init()