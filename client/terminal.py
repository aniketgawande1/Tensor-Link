from client.grpc_client import ChatClient


class Terminal:

    def __init__(self, username, room):

        self.client = ChatClient(username, room)

    def start(self):

        self.client.start()

        print("Connected")
        print("Type /quit to exit.\n")

        while True:

            text = input("> ")

            if text == "/quit":
                self.client.close()
                break

            if not text.strip():
                continue

            self.client.send(text)