import re


# Iterate message, determine type and return parsed data
def parse(raw):
    tags = {}
    for tag in iter(raw.split(';')):
        key, val = tag.split("=")
        if key == 'badges':
            tags[key] = parseBadges(val)
        else:
            tags[key] = val
    return tags

def parseBadges(raw):
    badges = {}
    if len(raw.strip()) > 0:
        for badge in raw.split(","):
            key, val = badge.split("/")
            badges[key] = val
    return badges
