from csv import DictWriter
from disco.types.message import Message

def toCSVLine(writer, msg):
    """
        Writes message object to a CSV line

        writer: csv.DictWriter
        msg: disco.types.message.Message
    """
    if isinstance(writer, DictWriter) and isinstance(msg, Message):
        writer.writerow({
            'id': msg.id,
            'type': str(msg.type),
            'author': str(msg.author.username) + '#' + str(msg.author.discriminator),
            'content': msg.with_proper_mentions,
            'timestamp': str(msg.timestamp),
            'edited_timestamp': str(msg.edited_timestamp),
            'mention_everyone': str(msg.mention_everyone),
            'pinned': str(msg.pinned),
            'mentions': len(msg.mentions.keys()),
            'mention_roles': len(msg.mention_roles),
            'embeds': len(msg.embeds),
            'attachments': len(msg.attachments.keys()),
            'reactions': len(msg.reactions)
        })
        