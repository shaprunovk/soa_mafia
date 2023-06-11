import threading
import grpc

import proto.game_pb2 as game
import proto.game_pb2_grpc as rpc

from game_config import config
from commands import client_commands

HOST = 'localhost'
PORT = config.PORT

class Client:

    def __init__(self, nickname: str):
        self.nickname = nickname
        channel = grpc.insecure_channel(HOST + ':' + str(PORT))
        self.conn = rpc.GameServerStub(channel)
        self.id = self.conn.Connect(game.Connection(nickname=nickname)).player_id
        threading.Thread(target=self.listen, daemon=True).start()
        self.write()

    def message_handler(self, Message):
        if self.id == Message.player_id or (Message.to and self.id not in Message.to):
            return
        if Message.name:
            print(f"{Message.name}: {Message.message}")
        else:
            print(f"{Message.message}")

    def listen(self):
        for Message in self.conn.GameStream(game.Empty()):
            self.message_handler(Message)

    def write(self):
        while True:
            message = input()
            if message:
                n = game.Message(
                    name=self.nickname, player_id=self.id, message=message
                )
                self.conn.SendMessage(n)
                if message == client_commands.LEAVE:
                    break


if __name__ == '__main__':
    nickname = input("Enter your nickname:\n")
    client = Client(nickname)
