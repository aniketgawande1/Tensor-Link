"""
gRPC Chat Service
"""

from concurrent.futures import ThreadPoolExecutor
import threading
import time
from generated import chat_pb2
from generated import chat_pb2_grpc

from server.managers.connection_manager import ConnectionManager

manager = ConnectionManager()


class ChatService(chat_pb2_grpc.ChatServiceServicer):

    def Chat(self, request_iterator, context):

        try:
            first_message = next(request_iterator)
        except StopIteration:
            return

        username = first_message.username
        room = first_message.room

        client = manager.connect(username, room)

        print(f"{username} joined {room}")

        # Unblock the queue and exit the handler loop when client cancels/disconnects
        context.add_callback(lambda: client.outgoing.put(None))

        def receive_messages():

            try:
                for message in request_iterator:

                    print(
                        f"[{message.room}] "
                        f"{message.username}: "
                        f"{message.message}"
                    )

                    manager.broadcast(
                        message.room,
                        message,
                    )

            finally:
                manager.disconnect(username)

                print(f"{username} disconnected")

        threading.Thread(
            target=receive_messages,
            daemon=True,
        ).start()

        while context.is_active():

            try:
                message = client.receive()

                if message is None:
                    break

                yield message

            except Exception:
                break