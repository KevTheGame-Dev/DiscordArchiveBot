import json
from disco.bot import Plugin
from disco.client import ClientConfig, Client
from disco.types.channel import MessageIterator
from disco.types.permissions import Permissions

with open('./config.json') as file:
    data = json.load(file)
AUTH_TOKEN = data['token']

aConfig = ClientConfig()
aConfig.token = AUTH_TOKEN
aClient = Client(aConfig)

def messageToJSON(self, msgObj):
    #Helper function. Recieves a Disco msg object and creates a mirror JSON object
    """ tempData = {}
    tempData['id'] = msgObj.id
    tempData['channel_id'] = msgObj.channel_id
    tempData['author'] = {}
    tempData['author']['id'] = msgObj.author.id
    tempData['author']['username'] = msgObj.author.username
    tempData['content'] = msgObj.content
    tempData['nonce'] = msgObj.nonce
    tempData['timestamp'] = msgObj.timestamp
    tempData['edited_timestamp'] = msgObj.edited_timestamp """
    tempData = vars(msgObj)
    print(json.dumps(tempData))
    return

class ArchivePlugin(Plugin):
    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')

    @Plugin.command('archive')
    def command_archive(self, event):
        #Get all messages from the channel this command is called in
        channel = event.channel
        
        #check if user calling archive is an admin
        if(not channel.get_permissions(event.member.user).can(Permissions.MANAGE_MESSAGES)):
            event.msg.reply('Only admins can archive channels.')
            return

        #Get all messages in the channel
        messages = []
        m_iter = MessageIterator(aClient, channel, 'DOWN', True, None, 0)#Message iterator obj uses pagination. Max buffer size is 100
        while True:
            notEmpty = m_iter.fill() #Fills the buffer, returns whether buffer has items
            if(notEmpty):#if buffer not empty
                temp_mgs = m_iter.next()
                for m in range(0, len(temp_mgs)):
                    messages.append(temp_mgs[m])#append each message to message list
            else:#if buffer is empty, all messages have been retrieved
                break

        #Process messages into file
        filename = 'data' + str(channel.id) + '.json' #All filenames will be unique
        #with open('data.json', 'w') as output:
        #    json.dump(messages.__dict__, output)
        #for message in messages:
        #    print(message.content)

        event.member.user.open_dm().send_message(messages[0].__str__())
        messageToJSON(self, messages[0])