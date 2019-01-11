import json
from disco.types.message import Message

def messageToDict(message):
    tempMessage = {}
    #Basic metrics for all messages
    tempMessage['message_id'] = message.id
    tempMessage['author'] = {}
    tempMessage['author']['id'] = message.author.id
    tempMessage['author']['username'] = message.author.username
    tempMessage['content'] = message.with_proper_mentions
    tempMessage['timestamp'] = str(message.timestamp)
    tempMessage['edited_timestamp'] = str(message.edited_timestamp)

    #
    """ if(False):#len(message.embeds) > 0):
        tempMessage['embeds'] = []
        for e in range(0, len(message.embeds)):
            temp_embed = embedToDict(message.embeds[e])#convert the embed to a Dict
            tempMessage['embeds'].append(temp_embed) """
    return tempMessage

