from disco.bot import Plugin

class HelpPlugin(Plugin):
    @Plugin.command('help')
    def command_ping(self, event):
        event.msg.reply("You don't need help!")