import json
import enum

from disco.types.message import *
from disco.types.user import User
from disco.types.guild import Role
from disco.types.base import (ListField, AutoDictField)

class UserEncoder(json.JSONEncoder):
    def default(self, user):
        if isinstance(user, User):
            return {
                'id': user.id,
                'username': str(user.username),
                'avatar': str(user.get_avatar_url()),
                'discriminator': str(user.discriminator),
                'bot': str(user.bot)
            }
        return json.JSONEncoder.default(self, user)

class MessageEmbedFooterEncoder(json.JSONEncoder):
    def default(self, embedFooter):
        if isinstance(embedFooter, MessageEmbedFooter):
            return {
                'text': embedFooter.icon_url,
                'icon_url': embedFooter.icon_url,
                'proxy_icon_url': embedFooter.proxy_icon_url
            }
        return json.JSONEncoder.default(self, embedFooter)
class MessageEmbedImageEncoder(json.JSONEncoder):
    def default(self, embedImage):
        if isinstance(embedImage, MessageEmbedImage):
            return {
                'url': embedImage.url,
                'proxy_url': embedImage.proxy_url,
                'width': embedImage.width,
                'height': embedImage.height
            }
        return json.JSONEncoder.default(self, embedImage)
class MessageEmbedThumbnailEncoder(json.JSONEncoder):
    def default(self, embedThumbnail):
        if isinstance(embedThumbnail, MessageEmbedThumbnail):
            return {
                'url': embedThumbnail.url,
                'proxy_url': embedThumbnail.proxy_url,
                'width': embedThumbnail.width,
                'height': embedThumbnail.height
            }
        return json.JSONEncoder.default(self, embedThumbnail)
class MessageEmbedVideoEncoder(json.JSONEncoder):
    def default(self, embedVideo):
        if isinstance(embedVideo, MessageEmbedVideo):
            return {
                'url': embedVideo.url,
                'width': embedVideo.width,
                'height': embedVideo.height
            }
        return json.JSONEncoder.default(self, embedVideo)
class MessageEmbedAuthorEncoder(json.JSONEncoder):
    def default(self, embedAuthor):
        if isinstance(embedAuthor, MessageEmbedAuthor):
            return {
                'name': embedAuthor.name,
                'url': embedAuthor.url,
                'icon_url': embedAuthor.icon_url,
                'proxy_icon_url': embedAuthor.proxy_icon_url
            }
        return json.JSONEncoder.default(self, embedAuthor)
class MessageEmbedFieldEncoder(json.JSONEncoder):
    def default(self, embedField):
        if isinstance(embedField, MessageEmbedField):
            return {
                'name': embedField.name,
                'value': embedField.value,
                'inline': embedField.inline
            }
        return json.JSONEncoder.default(self, embedField)
class MessageEmbedEncoder(json.JSONEncoder):
    def default(self, embed):
        if isinstance(embed, MessageEmbed):
            return {
                'title': embed.title,
                'type': embed.type,
                'description': embed.description,
                'url': embed.url,
                'timestamp': str(embed.timestamp),
                'color': embed.color,
                'footer': MessageEmbedFooterEncoder,#Replace
                'thumbnail': MessageEmbedThumbnailEncoder,#Replace
                'video': MessageEmbedVideoEncoder,#Replace
                'author': MessageEmbedAuthorEncoder,#Replace
                'fields': MessageEmbedFieldEncoder#Replace
            }
        return json.JSONEncoder.default(self, embed)

class MessageAttachmentEncoder(json.JSONEncoder):
    def default(self, attachment):
        if isinstance(attachment, MessageAttachment):
            return {
                'id': attachment.id,
                'filename': attachment.filename,
                'url': attachment.url,
                'proxy_url': attachment.proxy_url,
                'size': attachment.size,
                'height': attachment.height,
                'width': attachment.width
            }
        return json.JSONEncoder.default(self, attachment)

class EmojiEncoder(json.JSONEncoder):
    def default(self, emoji):
        if isinstance(emoji, Emoji):
            return {
                'name': emoji.to_string(),
                'animated': emoji.animated 
            }
        return json.JSONEncoder.default(self, emoji)
class MessageReactionEncoder(json.JSONEncoder):
    def default(self, reaction):
        if isinstance(reaction, MessageReaction):
            return {
                'emoji': EmojiEncoder.default(self, reaction.emoji),
                'count': reaction.count
            }
        return json.JSONEncoder.default(self, reaction)

class RolesEncoder(json.JSONEncoder):
    def default(self, role):
        if isinstance(role, Role):
            return {
                'name': role.name
            }
        return json.JSONEncoder.default(self, role)

class _EncodeListEnum(Enum):
    Roles = 0
    Embeds = 1
    Attachments = 2
    Reactions = 3

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class MessageEncoder(json.JSONEncoder):
    def _encodeMentions(self, mentions):#Mentions:Dict
        temp_mentions = []
        for m in mentions:
            temp_mentions.append(UserEncoder.default(self, mentions[m]))
        return temp_mentions

    def _encodeList(self, e_list, enumName=_EncodeListEnum.Roles.name):#Roles:List
        temp_arr = []
        for x in range(0, len(e_list)):
            if(enumName is _EncodeListEnum.Roles.name):
                temp_arr.append(RolesEncoder.default(self, e_list[x]))
            elif(enumName is _EncodeListEnum.Embeds.name):
                temp_arr.append(MessageEmbedEncoder.default(self, e_list[x]))
            elif(enumName is _EncodeListEnum.Attachments.name):
                temp_arr.append(MessageAttachmentEncoder.default(self, e_list[x]))
            elif(enumName is _EncodeListEnum.Reactions.name):
                temp_arr.append(MessageReactionEncoder.default(self, e_list[x]))
        return temp_arr

    def _encodeEmbeds(self, embeds):#Embeds:List
        temp_embeds = []
        for e in range(0, len(embeds)):
            temp_embeds.append(MessageEmbedEncoder.default(self, embeds[e]))
        return temp_embeds

    def _encodeAttachments(self, attachments):#Attachments:List
        temp_attachments = []
        for a in range(0, len(attachments)):
            temp_attachments.append(MessageAttachmentEncoder.default(self, attachments[a]))
        return temp_attachments

    def _encodeReactions(self, reactions):
        temp_reactions = []
        for r in range(0, len(reactions)):
            temp_reactions.append(MessageReactionEncoder.default(self, reactions[r]))
        return temp_reactions
        
    def default(self, msg):
        print(type(msg))
        if isinstance(msg, Message):
            return {
                'id': msg.id,
                'type': str(msg.type),
                'author': UserEncoder.default(self, msg.author),
                'content': msg.with_proper_mentions,
                'timestamp': str(msg.timestamp),
                'edited_timestamp': str(msg.edited_timestamp),
                'mention_everyone': str(msg.mention_everyone),
                'pinned': str(msg.pinned),
                'mentions': MessageEncoder._encodeMentions(self, msg.mentions),
                'mention_roles': MessageEncoder._encodeList(self, msg.mention_roles, _EncodeListEnum.Roles.name),
                'embeds': MessageEncoder._encodeList(self, msg.embeds, _EncodeListEnum.Embeds.name),
                'attachments': MessageEncoder._encodeList(self, msg.attachments, _EncodeListEnum.Attachments.name),
                'reactions': MessageEncoder._encodeList(self, msg.reactions, _EncodeListEnum.Reactions.name)
            }
        return json.JSONEncoder.default(self, msg)