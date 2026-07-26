import queue
import threading
import time

import grpc

from generated import chat_pb2
from generated import chat_pb2_grpc


class ChatClient:

    def __init__(self, username, room):

        self.username = username
        self.room = room

        self.channel = grpc.insecure_channel("localhost:50051")

        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)

        self.outgoing = queue.Queue()

    def request_generator(self):

        # Initial JOIN message
        yield chat_pb2.ChatMessage(
            username=self.username,
            room=self.room,
            message="joined",
            timestamp=int(time.time()),
            type=chat_pb2.JOIN,
        )

        while True:
            message = self.outgoing.get()

            if message is None:
                break

            yield message

    def start(self):

        responses = self.stub.Chat(self.request_generator())

        threading.Thread(
            target=self.receive_messages,
            args=(responses,),
            daemon=True,
        ).start()

    def receive_messages(self, responses):

        try:

            for message in responses:

                print(f"\n[{message.username}] {message.message}")

        except grpc.RpcError:

            print("Disconnected from server.")

    def send(self, text):

        self.outgoing.put(
            chat_pb2.ChatMessage(
                username=self.username,
                room=self.room,
                message=text,
                timestamp=int(time.time()),
                type=chat_pb2.CHAT,
            )
        )

    def close(self):

        self.outgoing.put(None)