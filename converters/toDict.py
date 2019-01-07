import json

def messageToDict(message):
    tempMessage = {}
    tempMessage['message_id'] = message.id
    tempMessage['author'] = {}
    tempMessage['author']['id'] = message.author.id
    tempMessage['author']['username'] = message.author.username
    tempMessage['content'] = message.with_proper_mentions
    tempMessage['timestamp'] = str(message.timestamp)
    tempMessage['edited_timestamp'] = str(message.edited_timestamp)
    return tempMessage