"""
Connection Manager

Maintains all active client connections.
Responsible for broadcasting messages to rooms.
"""

from __future__ import annotations

import queue
import threading
from collections import defaultdict
from typing import Dict, Set

from generated import chat_pb2


class ClientConnection:
    """
    Represents one connected client.
    """

    def __init__(self, username: str, room: str):
        self.username = username
        self.room = room

        # Messages destined for this client.
        self.outgoing = queue.Queue()

    def send(self, message: chat_pb2.ChatMessage):
        self.outgoing.put(message)

    def receive(self):
        return self.outgoing.get()


class ConnectionManager:

    def __init__(self):

        self._lock = threading.Lock()

        # username -> connection
        self.connections: Dict[str, ClientConnection] = {}

        # room -> usernames
        self.rooms: Dict[str, Set[str]] = defaultdict(set)

    def connect(self, username: str, room: str) -> ClientConnection:

        client = ClientConnection(username, room)

        with self._lock:
            # If the user is already connected, force disconnect the old one
            if username in self.connections:
                old_client = self.connections[username]
                old_client.outgoing.put(None)
                self.rooms[old_client.room].discard(username)
                if not self.rooms[old_client.room]:
                    del self.rooms[old_client.room]

            self.connections[username] = client
            self.rooms[room].add(username)

        return client

    def disconnect(self, username: str):

        with self._lock:

            if username not in self.connections:
                return

            room = self.connections[username].room

            del self.connections[username]

            self.rooms[room].discard(username)

            if not self.rooms[room]:
                del self.rooms[room]

    def broadcast(self, room: str, message: chat_pb2.ChatMessage):

        with self._lock:

            usernames = list(self.rooms.get(room, []))

        for username in usernames:

            connection = self.connections.get(username)

            if connection:
                connection.send(message)

    def users(self, room: str):

        with self._lock:
            return list(self.rooms.get(room, []))