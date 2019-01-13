import json
from enum import Enum

from disco.types.message import (Message, MessageAttachment, MessageEmbed,
 MessageEmbedAuthor, MessageEmbedField, MessageEmbedFooter, MessageEmbedImage,
  MessageEmbedThumbnail, MessageEmbedVideo, MessageReaction, MessageReactionEmoji, Emoji)
from disco.types.user import User
from disco.types.guild import Role
from disco.types.base import (ListField, AutoDictField, Unset)


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
            _fields = []
            for x in range(0, len(embed.fields)):
                _fields.append(MessageEmbedFieldEncoder.default(self, embed.fields[x]))
            return {
                'title': embed.title,
                'type': embed.type,
                'description': embed.description,
                'url': embed.url,
                'timestamp': str(embed.timestamp),
                'color': embed.color,
                'footer': MessageEmbedFooterEncoder.default(self, embed.footer),
                'thumbnail': MessageEmbedThumbnailEncoder.default(self, embed.thumbnail),
                'video': MessageEmbedVideoEncoder.default(self, embed.video),
                'author': MessageEmbedAuthorEncoder.default(self, embed.author),
                'fields': _fields
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
    Reactions = 2


class _EncodeDictEnum(Enum):
    Mentions = 0
    Attachments = 1


class MessageEncoder(json.JSONEncoder):
    def _encodeDict(self, e_dict, enumName):#Mentions:Dict
        temp_arr = []
        for m in e_dict:
            if(enumName is _EncodeDictEnum.Mentions.name):
                temp_arr.append(UserEncoder.default(self, e_dict[m]))
            elif(enumName is _EncodeDictEnum.Attachments.name):
                temp_arr.append(MessageAttachmentEncoder.default(self, e_dict[m]))
        return temp_arr

    def _encodeList(self, e_list, enumName):#Roles:List
        temp_arr = []
        for x in range(0, len(e_list)):
            if(enumName is _EncodeListEnum.Roles.name):
                temp_arr.append(RolesEncoder.default(self, e_list[x]))
            elif(enumName is _EncodeListEnum.Embeds.name):
                temp_arr.append(MessageEmbedEncoder.default(self, e_list[x]))
            elif(enumName is _EncodeListEnum.Reactions.name):
                temp_arr.append(MessageReactionEncoder.default(self, e_list[x]))
        return temp_arr
        
    def default(self, msg):
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
                'mentions': MessageEncoder._encodeDict(self, msg.mentions, _EncodeDictEnum.Mentions.name),
                'mention_roles': MessageEncoder._encodeList(self, msg.mention_roles, _EncodeListEnum.Roles.name),
                'embeds': MessageEncoder._encodeList(self, msg.embeds, _EncodeListEnum.Embeds.name),
                'attachments': MessageEncoder._encodeDict(self, msg.attachments, _EncodeDictEnum.Attachments.name),
                'reactions': MessageEncoder._encodeList(self, msg.reactions, _EncodeListEnum.Reactions.name)
            }
        if isinstance(msg, Unset):
            return None
        return json.JSONEncoder.default(self, msg)