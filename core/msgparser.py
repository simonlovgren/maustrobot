import re

# Server message
SRV_MSG = re.compile("^:([a-zA-Z0-9\.].*)\s([0-9]{3}).*:(.*)$")

# Tags
TAGS = re.compile("")

# User messages
PRVMSG = re.compile("")

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

		# Match tags
		try:
			m = TAGS.match(line)
			host, code, msg = m.group(1,2,3)
			parsed.append({"type":"tags"})
			continue
		except:
			pass

		# Match message
		try:
			m = MSG.match(line)
			host, code, msg = m.group(1,2,3)
			parsed.append({"type":"message"})
			continue
		except:
			pass

		# No match found
		parsed.append({"type":"unknown"})

	return parsed