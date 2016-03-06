# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import select
import socket
import sys
from util import flatten_parameters_to_string

""" @author: Aron Nieminen, Mojang AB"""


class RequestError(Exception):
    pass


class Connection(object):
    """Connection to a Minecraft Pi game"""
    RequestFailed = "Fail"

    def __init__(self, address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.last_sent = ""

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)
            e = "Drained Data: <%s>\n" % data.strip()
            e += "Last Message: <%s>\n" % self.last_sent.strip()
            sys.stderr.write(e)

    def send(self, f, *data):
        """Sends data. Note that a trailing newline '\n' is added here"""
        s = "%s(%s)\n" % (f, flatten_parameters_to_string(data))
        #print "f, data:", f, data
        #print "s", s
        self.drain()
        self.last_sent = s
        self.socket.sendall(s)

    def receive(self):
        """Receives data. Note that the trailing newline '\n' is trimmed"""
        s = self.socket.makefile("r").readline().rstrip("\n")
        if s == Connection.RequestFailed:
            raise RequestError("%s failed" % self.last_sent.strip())
        return s

    def send_receive(self, *data):
        """Sends and receive data"""
        self.send(*data)
        return self.receive()
