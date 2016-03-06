# -*- coding: utf-8 -*-
"""Minecraft PI low level api v0.1_1

Note: many methods have the parameter *arg. This solution makes it simple to
allow different types, and variable number of arguments.
The actual magic is a mix of flatten_parameters() and __iter__.
Example:
A Cube class could implement __iter__ to work in Minecraft.setBlocks(c, id).

(Because of this, it's possible to "erase" arguments. CmdPlayer removes
entity_id, by injecting [] that flattens to nothing)

@author: Aron Nieminen, Mojang AB

Updated to included additional functionality provided by RaspberryJuice:
- getBlocks() : implemented
- .create() : can now accept "name" (player name) for use in multiplayer
- CmdPositioner.getDirection
- CmdPositioner.getPitch
- CmdPositioner.getRotation
- getPlayerEntityId
- CmdEvents.pollChatPosts
"""
from __future__ import unicode_literals
import math

from connection import Connection
from vec3 import Vec3
from event import BlockEvent, ChatEvent
from block import Block
from util import flatten


def int_floor(*args):
    return [int(math.floor(arg)) for arg in flatten(args)]


class CmdPositioner(object):
    """Methods for setting and getting positions"""
    def __init__(self, connection, package_prefix):
        self.conn = connection
        self.pkg = package_prefix

    def getPos(self, entity_id):
        """Get entity position (entity_id:int) => Vec3
        getPos is deprecated and should not be used.
        Use get_pos instead.
        """
        return self.get_pos(entity_id)

    def get_pos(self, entity_id):
        """Get entity position (entity_id:int) => Vec3"""
        s = self.conn.send_receive(self.pkg + ".getPos", entity_id)
        return Vec3(*map(float, s.split(",")))

    def setPos(self, entity_id, *args):
        """Set entity position (entity_id:int, x,y,z)
        setPos is deprecated and should not be used.
        Use set_pos instead.
        """
        return self.set_pos(entity_id, *args)

    def set_pos(self, entity_id, *args):
        """Set entity position (entity_id:int, x,y,z)"""
        self.conn.send(self.pkg + ".setPos", entity_id, args)

    def getTilePos(self, entity_id):
        """Get entity tile position (entity_id:int) => Vec3
        getTilePos is deprecated and should not be used.
        Use get_tile_pos instead.
        """
        return self.get_tile_pos(entity_id)

    def get_tile_pos(self, entity_id):
        """Get entity tile position (entity_id:int) => Vec3"""
        s = self.conn.send_receive(self.pkg + ".getTile", entity_id)
        return Vec3(*map(int, s.split(",")))

    def setTilePos(self, entity_id, *args):
        """Set entity tile position (entity_id:int) => Vec3
        setTilePos is deprecated and should not be used.
        Use set_tile_pos instead.
        """
        return self.set_tile_pos(entity_id, *args)

    def set_tile_pos(self, entity_id, *args):
        """Set entity tile position (entity_id:int) => Vec3"""
        self.conn.send(self.pkg + ".setTile", entity_id, int_floor(*args))

    def getDirection(self, entity_id):
        """Get entity direction (entity_id:int) => Vec3
        getDirection is deprecated and should not be used.
        Use get_direction instead.
        """
        return self.get_direction(entity_id)

    def get_direction(self, entity_id):
        """Get entity direction (entity_id:int) => Vec3"""
        s = self.conn.send_receive(self.pkg + ".getDirection", entity_id)
        return Vec3(*map(float, s.split(",")))

    def getRotation(self, entity_id):
        """get entity rotation (entity_id:int) => float
        getRotation is deprecated and should not be used.
        Use get_rotation instead.
        """
        return self.get_rotation(entity_id)

    def get_rotation(self, entity_id):
        """get entity rotation (entity_id:int) => float"""
        return float(self.conn.send_receive(self.pkg + ".getRotation",
                                            entity_id))

    def getPitch(self, entity_id):
        """get entity pitch (entity_id:int) => float
        getPitch is deprecated and should not be used.
        Use get_pitch instead.
        """
        return self.get_pitch(entity_id)

    def get_pitch(self, entity_id):
        """get entity pitch (entity_id:int) => float"""
        return float(self.conn.send_receive(self.pkg + ".getPitch", entity_id))

    def setting(self, setting, status):
        """Set a player setting (setting, status). keys: autojump"""
        self.conn.send(self.pkg + ".setting", setting,
                       1 if bool(status) else 0)


class CmdEntity(CmdPositioner):
    """Methods for entities"""
    def __init__(self, connection):
        super(CmdEntity, self).__init__(connection, "entity")


class CmdPlayer(CmdPositioner):
    """Methods for the host (Raspberry Pi) player"""
    def __init__(self, connection, name=None):
        super(CmdPlayer, self).__init__(connection, "player")
        self.conn = connection
        self.name = name

    def getPos(self):
        """getPos is depreciated and should not be used.
        Use get_pos instead.
        """
        return self.get_pos()

    def get_pos(self):
        return super(CmdPlayer, self).get_pos(self.name)

    def setPos(self, *args):
        """setPos is deprecated and should not be used.
        Use setPos instead.
        """
        return self.set_pos(*args)

    def set_pos(self, *args):
        return super(CmdPlayer, self).set_pos(self.name, args)

    def getTilePos(self):
        """getTilePos is deprecated and should not be used.
        Use get_tile_pos instead.
        """
        return self.get_tile_pos()

    def get_tile_pos(self):
        return super(CmdPlayer, self).get_tile_pos(self.name)

    def setTilePos(self, *args):
        """setTilePos is deprecated and should not be used.
        Use set_tile_pos instead.
        """
        return self.set_tile_pos(self, *args)

    def set_tile_pos(self, *args):
        return super(CmdPlayer, self).set_tile_pos(self.name, args)

    def getDirection(self):
        """getDirection is deprecated and should not be used.
        Use get_direction instead.
        """
        return self.get_direction()

    def get_direction(self):
        return super(CmdPlayer, self).get_direction(self.name)

    def getRotation(self):
        """getRotation is deprecated and should not be used.
        Use get_rotation instead.
        """
        return self.get_rotation()

    def get_rotation(self):
        return super(CmdPlayer, self).get_rotation(self.name)

    def getPitch(self):
        """getPitch is deprecated and should not be used.
        Use get_pitch instead.
        """
        return super(CmdPlayer, self).get_pitch(self.name)


class CmdCamera(object):
    def __init__(self, connection):
        self.conn = connection

    def setNormal(self, *args):
        """Set camera mode to normal Minecraft view ([entity_id])
        setNormal is deprecated and should not be used.
        Use set_normal instead.
        """
        return self.set_normal(*args)

    def set_normal(self, *args):
        """Set camera mode to normal Minecraft view ([entity_id])"""
        self.conn.send("camera.mode.setNormal", args)

    def setFixed(self):
        """Set camera mode to fixed view
        setFixed is deprecated and should not be used.
        Use set_fixed instead.
        """
        return self.set_fixed()

    def set_fixed(self):
        """Set camera mode to fixed view"""
        self.conn.send("camera.mode.setFixed")

    def setFollow(self, *args):
        """Set camera mode to follow an entity ([entity_id])
        setFollow is deprecated and should not be used.
        Use set_follow instead.
        """
        return self.set_follow(*args)

    def set_follow(self, *args):
        """Set camera mode to follow an entity ([entity_id])"""
        self.conn.send("camera.mode.setFollow", args)

    def setPos(self, *args):
        """Set camera entity position (x,y,z)
        setPos is deprecated and should not be used.
        Use set_pos instead.
        """
        return self.set_pos(*args)

    def set_pos(self, *args):
        """Set camera entity position (x,y,z)"""
        self.conn.send("camera.setPos", args)


class CmdEvents(object):
    """Events"""
    def __init__(self, connection):
        self.conn = connection

    def clearAll(self):
        """Clear all old events
        clearAll is deprecated and should not be used.
        Use clear_all instead.
        """
        return self.clear_all()

    def clear_all(self):
        self.conn.send("events.clear")

    def pollBlockHits(self):
        """Only triggered by sword => [BlockEvent]
        pollBlockHits is deprecated and should not be used.
        Use poll_block_hits instead.
        """
        return self.poll_block_hits()

    def poll_block_hits(self):
        """Only triggered by sword => [BlockEvent]"""
        hits_str = self.conn.send_receive("events.block.hits")
        events = [evt for evt in hits_str.split("|") if evt]
        return [BlockEvent.hit(*map(int, evt.split(","))) for evt in events]

    def pollChatPosts(self):
        """Triggered by posts to chat => [ChatEvent]
        pollChatPosts is deprecated and should not be used.
        Use poll_chat_posts instead."""
        return self.poll_chat_posts()

    def poll_chat_posts(self):
        """Triggered by posts to chat => [ChatEvent]"""
        posts_str = self.conn.send_receive("events.chat.posts")
        events = [evt for evt in posts_str.split("|") if evt]
        return [ChatEvent.Post(int(evt[:evt.find(",")]),
                               evt[evt.find(",") + 1:]) \
                for evt in events]


class Minecraft(object):
    """The main class to interact with a running instance of Minecraft Pi."""
    def __init__(self, connection, name=None):
        self.conn = connection

        self.camera = CmdCamera(connection)
        self.entity = CmdEntity(connection)
        self.player = CmdPlayer(connection, name)
        self.events = CmdEvents(connection)

    def getBlock(self, *args):
        """Get block (x,y,z) => id:int
        getBlock is deprecated and should not be used.
        Use get_block instead."""
        return self.get_block(*args)

    def get_block(self, *args):
        """Get block (x,y,z) => id:int"""
        return int(self.conn.send_receive("world.getBlock", int_floor(args)))

    def getBlockWithData(self, *args):
        """Get block with data (x,y,z) => Block
        getBlockWithData is deprecated and should not be used.
        Use get_block_with_data instead.
        """
        return self.get_block_with_data(*args)

    def get_block_with_data(self, *args):
        """Get block with data (x,y,z) => Block"""
        ans = self.conn.send_receive("world.getBlockWithData", int_floor(args))
        return Block(*map(int, ans.split(",")))

    """
        @TODO
    """

    def getBlocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]
        getBlocks is deprecated and should not be used.
        Use get_blocks instead.
        """
        return self.get_blocks(*args)

    def get_blocks(self, *args):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [id:int]"""
        blocks_str = self.conn.send_receive("world.getBlocks", int_floor(args))
        return map(int, blocks_str.split(","))

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])
        setBlock is deprecated and should not be used.
        Use set_block instead.
        """
        return self.set_block(*args)

    def set_block(self, *args):
        """Set block (x,y,z,id,[data])"""
        self.conn.send("world.setBlock", int_floor(args))

    def setBlocks(self, *args):
        """Set a cuboid of blocks (x0, y0, z0, x1, y1, z1, id, [data])
        setBlocks is deprecated and should not be used.
        Use set_blocks instead.
        """
        return self.set_blocks(*args)

    def set_blocks(self, *args):
        """Set a cuboid of blocks (x0, y0, z0, x1, y1, z1, id, [data])"""
        self.conn.send("world.setBlocks", int_floor(args))

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int
        getHeight is deprecated and should not be used.
        Use get_height instead.
        """
        return self.get_height(*args)

    def get_height(self, *args):
        """Get the height of the world (x,z) => int"""
        return int(self.conn.send_receive("world.getHeight", int_floor(args)))

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]
        getPlayerEntityIds is deprecated and should not be used.
        Use get_player_entity_ids instead.
        """
        return self.get_player_entity_ids()

    def get_player_entity_ids(self):
        """Get the entity ids of the connected players => [id:int]"""
        ids = self.conn.send_receive("world.getPlayerIds")
        return map(int, ids.split("|"))

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]
        getPlayerEntityId is deprecated and should not be used.
        Use get_player_entity_id instead.
        """
        return self.get_player_entity_id(name)

    def get_player_entity_id(self, name):
        """Get the entity id of the named player => [id:int]"""
        return int(self.conn.send_receive("world.getPlayerId", name))

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world
        saveCheckpoint is deprecated and should not be used.
        Use save_checkpoint instead.
        """
        return self.save_checkpoint()

    def save_checkpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.conn.send("world.checkpoint.save")

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint
        restoreCheckpoint is deprecated and should not be used.
        Use restore_checkpoint instead.
        """
        return self.restore_checkpoint()

    def restore_checkpoint(self):
        """Restore the world state to the checkpoint"""
        self.conn.send("world.checkpoint.restore")

    def postToChat(self, msg):
        """Post a message to the game chat
        postToChat is deprecated and should not be used.
        Use post_to_chat instead.
        """
        return self.post_to_chat(msg)

    def post_to_chat(self, msg):
        """Post a message to the game chat"""
        self.conn.send("chat.post", msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status).
        keys: world_immutable, nametags_visible
        """
        self.conn.send("world.setting", setting, 1 if bool(status) else 0)

    @staticmethod
    def create(address="localhost", port=4711, name=None):
        return Minecraft(Connection(address, port), name)


if __name__ == "__main__":
    mc = Minecraft.create()
    mc.post_to_chat("Hello, Minecraft!")
