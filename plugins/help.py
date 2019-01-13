from disco.bot import Plugin
from disco.types.message import MessageEmbed
from datetime import datetime

embed = MessageEmbed()
embed.set_author(name="KevTheGame-Dev", url="https://github.com/KevTheGame-Dev")
embed.title = "ArchiveBot Help"
embed.description = "All commands start with @ArchiveBot \n _______________________"
embed.add_field(name='archive', value='Scrapes all messages in current channel and sends them to requester in a DM. Defaults to JSON \n Example: @Archivebot archive CSV', inline=False)
embed.add_field(name='\u200B', value='Optional Parameters:', inline=False)
embed.add_field(name='JSON', value='Archive file will be in JSON format', inline=True)
embed.add_field(name='CSV', value='Archive file will be in CSV format. Note that due to the nature of csv, some of the more detailed info is excluded', inline=True)

class HelpPlugin(Plugin):
    @Plugin.command('help')
    def command_ping(self, event):
        event.msg.reply(embed=embed)