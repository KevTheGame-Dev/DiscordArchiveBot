# DiscordArchiveBot
Discord Bot that creates message archive files of channels upon user request. 
Currently, the only archive format supported is JSON. Only admins of a server can use the archive function.

User Confidentiality: Message data is **not** stored permanently. Message data is processed, stored in a file which is then sent to the user. As soon as the bot recieves confirmation that the file has been sent to the user's direct messages, the file is promptly deleted. Message data is never used beyond this messure.


# Usage:

Before adding the bot to your server, please note that by default the bot recieves the following permissions:
1. Read Messages: Enables the bot to pull messages to create archive
2. Send Messages: Enables the bot to reply with the archive file
3. Attach Files: Enables the bot to attach the archive file
4. Read Message History: Enables the bot to access messages sent before the bot was added

These permissions can be modified when you add the bot, but without them be advised the bot will not function properly.


## Adding to Server:

Click [here](https://discordapp.com/oauth2/authorize?client_id=530822954544791562&scope=bot&permissions=101376) to add the bot. Make sure you're logged in.


## Commands:
#### Archive:
`@ArchiveBot archive`
Creates an archive file (csv), and DM's the requesting admin with the file
Planned: Supporting other file formats, such as CSV

#### Help:
`@ArchiveBot help`
Lists out all commands in chat


# Libraries Used:
[Disco](https://github.com/b1naryth1ef/disco) - A Discord Python library