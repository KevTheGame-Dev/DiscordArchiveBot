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


class ArchivePlugin(Plugin):
    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')

    @Plugin.command('archive')
    def command_archive(self, event):
        #Get all messages from the channel this command is called in
        channel = event.channel

        #check permissions
        if(not channel.get_permissions(event.member.user).can(Permissions.MANAGE_MESSAGES)):
            event.msg.reply('Only admins can archive channels.')
            return

        messages = []
        m_iter = MessageIterator(aClient, channel, 'DOWN', True, None, 0)

        while True:
            notEmpty = m_iter.fill() #Fills the buffer, returns whether buffer has items
            if(notEmpty):#if buffer not empty
                temp_mgs = m_iter.next()
                for m in range(0, len(temp_mgs)):
                    messages.append(temp_mgs[m])#append each message to message list
            else:#if buffer is empty, all messages have been retrieved
                break

        for message in messages:
            print(message.content)

        event.member.user.open_dm().send_message(messages[0].__str__())
        