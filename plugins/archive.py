import json
import csv
from os import path, remove
#from argparse import ArgumentParser

from disco.bot import Plugin
from disco.client import ClientConfig, Client, APIClient
from disco.types.channel import MessageIterator
from disco.types.permissions import Permissions
from datetime import datetime

from util.encoders import MessageEncoder
from util.toCSV import toCSVLine

with open('./config.json') as file:#Pull config variables from file
    data = json.load(file)
AUTH_TOKEN = data['token']
DEBUG = data['debug']

mConfig = ClientConfig()
mConfig.token = AUTH_TOKEN
mClient = Client(mConfig)


class ArchivePlugin(Plugin):
    @Plugin.command('ping')
    def command_ping(self, event):
        event.msg.reply('Pong!')

    @Plugin.command('archive', parser=True)
    @Plugin.parser.add_argument('--JSON', help="Archive in JSON format", action="store_true", default=False)
    @Plugin.parser.add_argument('--CSV', help="Archive in CSV format", action="store_true", default=False)
    def command_archive(self, event, args):
        #Ensure the user specifies what file format they want
        if not(args.JSON or args.CSV):
            event.msg.reply('`--JSON or --CSV flag required`')
        
        #Get all messages from the channel this command is called in
        channel = event.channel
        
        #check if user calling archive is an admin
        if(not channel.get_permissions(event.member.user).can(Permissions.MANAGE_MESSAGES)):
            event.msg.reply('Only admins can archive channels.')
            return

        #Get all messages in the channel
        messages = []
        m_iter = MessageIterator(self.bot.client, channel, 'DOWN', True, None, 0)#Message iterator obj uses pagination. Max buffer size is 100
        while True:
            notEmpty = m_iter.fill() #Fills the buffer, returns whether buffer has items
            if(notEmpty):#if buffer not empty
                temp_mgs = m_iter.next()
                for m in temp_mgs:
                    messages.append(m)#append to list
            else:#if buffer is empty, all messages have been retrieved
                break

        #Process messages into file
        """ All filenames include channel ID to be unique in the very unlikely chance that 2 calls for channels
            with the same name are made within the same small amount of time """
        filename = 'data' + str(channel.id) + '_' + str(channel)[1:] + str(datetime.now().date())

        #JSON
        if(args.JSON):
            with open(filename + '.json', 'w') as output:#Write to JSON file
                json.dump(messages, output, indent=4, cls=MessageEncoder)

            if(DEBUG):
                with open("_"+filename + '.json', 'w') as output:#Write to debug JSON file
                    json.dump(messages, output, indent=4, cls=MessageEncoder)

            with open(filename + '.json', 'r') as output:#Send file in DM to user
                deliverMsg = "Here's your archive of the " + str(channel) + " channel!"
                event.member.user.open_dm().send_message(deliverMsg, attachments=[(filename + '.json', output, 'application/json')])

            #Remove data file once sent
            if(path.exists(filename + '.json')):
                remove(filename + '.json')
            else:
                print("File does not exist")
        

        #CSV
        if(args.CSV):
            with open(filename + '.csv', 'w') as output:#Write to CSV file
                fields = ['id','type','author','content','timestamp','edited_timestamp','mention_everyone',
                            'pinned','mentions','mention_roles','embeds','attachments','reactions']
                writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
                writer.writeheader()
                for m in messages:
                    toCSVLine(writer, m)

            if(DEBUG):
                with open("_"+filename + '.csv', 'w') as output:#Write to debug CSV file
                    fields = ['id','type','author','content','timestamp','edited_timestamp','mention_everyone',
                            'pinned','mentions','mention_roles','embeds','attachments','reactions']
                    writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
                    writer.writeheader()
                    for m in messages:
                        toCSVLine(writer, m)

            with open(filename + '.csv', 'r') as output:#Send CSV file
                deliverMsg = "Here's your archive of the " + str(channel) + " channel!"
                event.member.user.open_dm().send_message(deliverMsg, attachments=[(filename + '.csv', output, 'text/csv')])
            
            #Remove data file once sent
            if(path.exists(filename + '.csv')):
                remove(filename + '.csv')
            else:
                print("File does not exist")
        
        