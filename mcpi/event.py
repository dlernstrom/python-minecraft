# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from vec3 import Vec3


class BlockEvent(object):
    """An Event related to blocks (e.g. placed, removed, hit)"""
    HIT = 0

    def __init__(self, type, x, y, z, face, entity_id):
        self.type = type
        self.pos = Vec3(x, y, z)
        self.face = face
        self.entity_id = entity_id

    def __repr__(self):
        s_type = {
            BlockEvent.HIT: "BlockEvent.HIT"
        }.get(self.type, "???")

        return "BlockEvent(%s, %d, %d, %d, %d, %d)" % (
            s_type, self.pos.x, self.pos.y, self.pos.z, self.face,
            self.entity_id)

    @staticmethod
    def hit(x, y, z, face, entity_id):
        return BlockEvent(BlockEvent.HIT, x, y, z, face, entity_id)


class ChatEvent(object):
    """An Event related to chat (e.g. posts)"""
    POST = 0

    def __init__(self, type, entity_id, message):
        self.type = type
        self.entity_id = entity_id
        self.message = message

    def __repr__(self):
        sType = {
            ChatEvent.POST: "ChatEvent.POST"
        }.get(self.type, "???")

        return "ChatEvent(%s, %d, %s)" % (
            sType, self.entity_id, self.message)

    @staticmethod
    def Post(entity_id, message):
        return ChatEvent(ChatEvent.POST, entity_id, message)
