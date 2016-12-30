import re
import core.tagparser

# Server message
SRV_MSG = re.compile("^:([a-zA-Z0-9\.].*?)\s([0-9]{3}).*?:(.*)$")

# Membership events

# JOIN
# :maustronaut!maustronaut@maustronaut.tmi.twitch.tv JOIN #maustronaut
JOIN = re.compile("^:(.*?)!(.*?)@([a-zA-Z0-9\.].*?)\sJOIN\s(.*?)$")

# MODE
#:jtv MODE #channel +o operator_user
MODE = re.compile("^:jtv\sMODE\s([a-zA-Z0-9#]*?)\s(\+|-)(.*?)\s(.*)$")

# User messages
# @badges=broadcaster/1;color=#D2691E;display-name=Maustronaut;emotes=;id=7e158278-ebb7-4904-afc4-164e1b510d48;mod=0;room-id=81519801;sent-ts=1482920324097;subscriber=0;tmi-sent-ts=1482920323924;turbo=0;user-id=81519801;user-type= :maustronaut!maustronaut@maustronaut.tmi.twitch.tv PRIVMSG #maustronaut :asdf
PRVMSG = re.compile("^@(.*?)\s:(.*?)!.*?\sPRIVMSG\s(.*?)\s:(.*?)$")

# Whisper
# @badges=;color=#D2691E;display-name=Maustronaut;emotes=;message-id=2;thread-id=81519801_100697592;turbo=0;user-id=81519801;user-type= :maustronaut!maustronaut@maustronaut.tmi.twitch.tv WHISPER maustrobot :ping
WHISPER = re.compile("^@(.*?)\s:(.*?)!.*?\sWHISPER\s(.*?)\s:(.*?)$")

# Allow iterating over lines in message
def scanLines(message):
    return iter(message.splitlines())

# Iterate message, determine type and return parsed data
def parseMessage(message):
    parsed = []
    message = scanLines(message)
    for line in message:
        # Match server message
        try:
            m = SRV_MSG.match(line)
            host, code, msg = m.group(1,2,3)
            parsed.append({"type":"server", "host":host, "code":code, "message":msg})
            continue
        except:
            pass

        # Membership events

        # Match JOIN
        try:
            m = JOIN.match(line)
            user, host, channel = m.group(1,3,4)
            parsed.append({"type":"join", "host":host, "user":user, "channel":channel})
            continue
        except:
            pass


        # Match MODE
        try:
            m = MODE.match(line)
            channel, action, operator, user = m.group(1,2,3,4)
            parsed.append({"type":"mode", "channel":channel, "action":(1 if action == '+' else 0), "operator":operator, "user":user})
            continue
        except:
            pass

        # Match message
        try:
            m = PRVMSG.match(line)
            tags, user, channel, msg = m.group(1,2,3,4)
            parsed.append({"type":"message", "tags":core.tagparser.parse(tags), "channel":channel, "user":user, "message":msg})
            continue
        except:
            pass

        # Match whisper
        try:
            m = WHISPER.match(line)
            tags, fromuser, touser, msg = m.group(1,2,3,4)
            parsed.append({"type":"whisper", "tags":core.tagparser.parse(tags), "to":touser, "from":fromuser, "message":msg})
            continue
        except:
            pass

        
        # No match found
        parsed.append({"type":"unknown"})

    return parsed
