from concurrent import futures

import grpc

from generated import chat_pb2_grpc
from server.services.chat_service import ChatService


HOST = "0.0.0.0"
PORT = 50051


def create_server():

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=20)
    )

    chat_pb2_grpc.add_ChatServiceServicer_to_server(
        ChatService(),
        server,
    )

    server.add_insecure_port(f"{HOST}:{PORT}")

    return server