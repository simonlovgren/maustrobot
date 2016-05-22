# Maustrobot IRC Bot (for Twitch)
IRC bot (primarily) for Twitch.

The bot is completely modular, adding a new command is simply
adding a new script (or folder) within the `commands`-folder
and the same goes for rules (`rules`-folder).

***

**This is a work in progress and is currently only single-instance
*(aka. no separate threads handling messages and only able to join
a single channel)*.**

***

## Current capability
- Authenticating to Twitch IRC servers
- Responding to `ping` messages

## Structure
```
root
| -- bot.py
| -- bot.conf
| -- channels.conf
| -- core
| -- rules
     | -- my_rule.py
     | -- my_other_rule
          | -- my_other_rule.py
| -- commands
     | -- my_cmd.py
     | -- my_other_cmd
          | -- my_other_cmd.py
```
### root
#### bot.py
This is the main star-file of the bot.

#### bot.conf
This is the config-file for all settings of the bot.

| Setting  | Description                         |
| -------- | ----------------------------------- |
| host     | Host server (eg. *irc.twitch.tv*).  |
| port     | Server port (eg. *6667*).           |
| nick     | Nickname for the bot.               |
| password | OAuth-key for authenticating.       |
| channel  | Channel to join.                    |

#### channels.conf
**Currently not in use**  
Will, in the future, contain a list of all channels to join on start.

### core
Core files of the bot. Handles incoming messages, dispatch to correct
command- or rule script.

### rules
Rules to be automatically applied/enforced upon chat messages. For
example deleting messages containing links.

### commands
Commands which may be invoked by keywords in messages (eg. `!ping`, `!info`, etc.)
