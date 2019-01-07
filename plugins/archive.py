import json
from os import path, remove
from disco.bot import Plugin
from disco.client import ClientConfig, Client
from disco.types.channel import MessageIterator
from disco.types.permissions import Permissions
from datetime import datetime

from converters.toDict import messageToDict

with open('./config.json') as file:
    data = json.load(file)
AUTH_TOKEN = data['token']

aConfig = ClientConfig()
aConfig.token = AUTH_TOKEN
aClient = Client(aConfig)


class ArchivePlugin(Plugin):
    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')

    @Plugin.command('archive')
    def command_archive(self, event):
        #Get all messages from the channel this command is called in
        channel = event.channel
        print(channel)
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
                    msg_Dict = messageToDict(temp_mgs[m])
                    messages.append(msg_Dict)#append each message to message list
            else:#if buffer is empty, all messages have been retrieved
                break

        #Process messages into file
        """ All filenames include channel ID to be unique in the very unlikely chance that 2 calls for channels
            with the same name are made within the same small amount of time """
        filename = 'data' + str(channel.id) + '_' + str(channel)[1:] + str(datetime.now().date()) + '.json'
        print(filename)
        with open(filename, 'w') as output:
            json.dump(messages, output, indent=4)
        with open(filename, 'r') as output:
            deliverMsg = "Here's your archive of the " + str(channel) + " channel!"
            event.member.user.open_dm().send_message(deliverMsg, attachments=[(filename, output, 'application/json')])
        
        #Remove data file once sent
        if(path.exists(filename)):
            remove(filename)
        else:
            print("File does not exist")

        