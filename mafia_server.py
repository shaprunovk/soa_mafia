import time
import random
import threading

import grpc
import proto.game_pb2 as game
import proto.game_pb2_grpc as rpc

from game_config import config
from mafia_commands import client_commands
from concurrent import futures
from collections import Counter


class Member:
    _counter = 0

    def __init__(self, nickname):
        Member._counter += 1
        self._nickname = nickname
        self._player_id = self._counter
        self._status = None
        self._role = None

    def prepare(self, role):
        self._role = role
        self._status = "alive"

    def dead(self):
        self._status = "dead"
        self._role = "ghost"

    @property
    def nickname(self):
        return self._nickname

    @property
    def player_id(self):
        return self._player_id

    @property
    def role(self):
        return self._role

    @property
    def status(self):
        return self._status


class GameServer(rpc.GameServerServicer):

    def __init__(self, size):
        self.members = {}
        self.messages_internal = []
        self.size = size

        self._game_running = False
        self._voting = []
        self._voted = []
        self._active_role = None
        self._time = None

    def set_default(self):
        self._time = None
        self._voted = []
        self._voting = []
        self._active_role = None
        self._time = None

    def GameStream(self, request_iterator, context):
        lastindex = 0
        while True:
            while len(self.messages_internal) > lastindex:
                n = self.messages_internal[lastindex]
                lastindex += 1
                yield n

    def SendMessage(self, request: game.Message, context):
        self.message_handler(request)
        return game.Empty()

    def Connect(self, request: game.Connection, context):
        m = Member(request.nickname)
        self.members[m.player_id] = m
        n = game.Message(message=f"{m.nickname} joined!")
        self.messages_internal.append(n)
        if len(self.members) == self.size:
            threading.Thread(target=self.start_game).start()
        return game.ConnectionReply(player_id=m.player_id)

    def serialize_members(self, m):
        members_text = "ID\tNAME"
        if self._game_running:
            members_text += "\tROLE\tSTATUS"
        members_text += "\n"
        for member in self.members.values():
            members_text += f"{member.player_id}\t{member.nickname}"
            if self._game_running:
                if m.status == "alive":
                    members_text += f"\t???\t{member.status}"
                else:
                    members_text += f"\t{member.role}\t{member.status}"
            if member.player_id == m.player_id:
                members_text += " << YOU"
            members_text += "\n"
        return members_text

    def members_with_role(self, role, self_id):
        mafia_ids = []
        for member in self.members.values():
            if member.role == role and member.player_id != self_id:
                mafia_ids.append(member.player_id)
        if not mafia_ids:
            mafia_ids = [-1]
        return mafia_ids

    def members_with_status(self, status, self_id):
        mafia_ids = []
        for member in self.members.values():
            if member.status == status and member.player_id != self_id:
                mafia_ids.append(member.player_id)
        if not mafia_ids:
            mafia_ids = [-1]
        return mafia_ids

    def message_handler(self, Message: game.Message):
        if Message.message.startswith(client_commands.MEMBERS):
            self.send_message(self.serialize_members(self.members[Message.player_id]), Message.player_id)
        elif Message.message.startswith(client_commands.LEAVE):
            left_member = self.members[Message.player_id]
            self.members.pop(Message.player_id)
            if self._game_running:
                self.set_default()
                self.send_message("GAME STOPPED")
            self.send_message(f"{left_member.nickname} left")
        elif Message.message.startswith(client_commands.HELP):
            self.send_message(client_commands.COMMANDS_LIST, Message.player_id)
        elif Message.message.startswith(client_commands.SELF):
            if self._game_running:
                self.send_message(f"YOU ARE {self.members[Message.player_id].role}", Message.player_id)
        elif Message.message.startswith(client_commands.READY):
            if self._game_running:
                return
            if Message.player_id not in self._voted:
                self._voted.append(Message.player_id)
                self.send_message(f"{self.members[Message.player_id].nickaname} is ready to start game")
        elif Message.message.startswith(client_commands.KILL):
            if self._game_running:
                member = self.members[Message.player_id]
                if member.role == self._active_role \
                        and member.player_id not in self._voted \
                        and member.status == "alive":
                    try:
                        victim_id = int(Message.message.split(" ")[1])
                        self._voted.append(member.player_id)
                        self._voting.append(victim_id)
                        self.send_message(
                            f"{member.nickname} is voted for {self.members[victim_id].nickname}",
                            self.members_with_role(member.role, member.player_id)
                        )
                    except:
                        self.send_message("INCORRECT VICTIM ID", Message.player_id)
        elif Message.message.startswith(client_commands.EXECUTE):
            if self._game_running:
                member = self.members[Message.player_id]
                if self._time == "day" and Message.player_id not in self._voted and member.status == "alive":
                    try:
                        victim_id = int(Message.message.split(" ")[1])
                        self._voted.append(Message.player_id)
                        self._voting.append(victim_id)
                        self.send_message(f"{member.nickname} is voted for {self.members[victim_id].nickname}")
                    except:
                        self.send_message("INCORRECT VICTIM ID", Message.player_id)
        elif Message.message.startswith(client_commands.SKIP):
            if self._game_running:
                member = self.members[Message.player_id]
                if self._time == "day" and Message.player_id not in self._voted and member.status == "alive":
                    try:
                        self._voted.append(Message.player_id)
                        self._voting.append(0)
                        self.send_message(f"{member.nickname} is voted for skipping execution")
                    except:
                        self.send_message("INCORRECT VICTIM ID", Message.player_id)
        elif Message.message.startswith(client_commands.VERIFY):
            if self._game_running:
                if self.members[Message.player_id].role == self._active_role \
                        and self._active_role == "policeman" \
                        and Message.player_id not in self._voted \
                        and self.members[Message.player_id].status == "alive":
                    victim_id = int(Message.message.split(" ")[1])
                    victim = self.members[victim_id]
                    self.send_message(f"{victim.nickname} IS {victim.role}", Message.player_id)
        elif self._game_running:
            member = self.members[Message.player_id]
            if self._time == "night" and member.role != "citizen":
                n = game.Message(
                    player_id=Message.player_id, name=Message.name, message=Message.message,
                    to=self.members_with_role(member.role, member.player_id)
                )
                self.messages_internal.append(n)
            elif self._time == "day":
                n = game.Message(
                    player_id=Message.player_id, name=Message.name, message=Message.message,
                    to=self.members_with_status(member.status, member.player_id)
                )
                self.messages_internal.append(n)
        else:
            self.messages_internal.append(Message)

    def send_message(self, text, to=None):
        if type(to) != list and to:
            to = [to]
        n = game.Message(message=text, to=to)
        self.messages_internal.append(n)

    def start_game(self):
        self._game_running = True
        self._voted = []
        distribution = []
        mafia_count = self.size // 3
        for i in range(mafia_count):
            distribution.append("mafia")
        distribution.append("policeman")
        citizens_count = self.size - mafia_count - 1
        for i in range(citizens_count):
            distribution.append("citizen")
        random.shuffle(distribution)

        count = {
            "mafia": mafia_count,
            "policeman": 1,
            "citizen": citizens_count
        }
        wait_mafia = mafia_count * 15
        wait_policeman = 15
        wait_all = 15 * self.size

        self.send_message("STARTING GAME")
        self.send_message(".\n" * 5)
        for i, member in enumerate(self.members.values()):
            member.prepare(distribution[i])
            self.send_message(f"YOU ARE {member.role}", member.player_id)

        self.send_message("IF YOU DON'T KNOW COMMANDS TYPE '/help' TO SEE LIST OF COMMANDS\n")

        time.sleep(1)
        while count["mafia"] < count["citizen"] + count["policeman"] and count["mafia"] != 0:
            self._time = "night"
            self.send_message("THE CITY FALLS ASLEEP, BUT...")
            self._active_role = "mafia"
            self.send_message("MAFIA IS NEVER SLEEPS")
            time.sleep(wait_mafia)
            mafia_killed = None
            if self._voting:
                v = Counter(self._voting)
                mafia_killed = list(v.keys())[0]
                self._voting = []
                self._voted = []
            self.send_message("\nMAFIA FINISHED\n")
            time.sleep(1)

            self.send_message("POLICEMAN WOKE UP TO FIND MAFIA")
            self._active_role = "policeman"
            time.sleep(wait_policeman)
            policeman_killed = None
            if self._voting:
                policeman_killed = self._voting[0]
                self._voting = []
                self._voted = []
            self.send_message("POLICEMAN FINISHED")
            time.sleep(1)

            dead_list = "TONIGHT WE LOST:\n"
            if mafia_killed:
                if self.members[mafia_killed].status == "alive":
                    role = self.members[mafia_killed].role
                    self.members[mafia_killed].dead()
                    count[role] -= 1
                    dead_list += f" - {self.members[mafia_killed].nickname}\n"
            if policeman_killed:
                if self.members[policeman_killed].status == "alive":
                    role = self.members[policeman_killed].role
                    self.members[policeman_killed].dead()
                    count[role] -= 1
                    dead_list += f" - {self.members[policeman_killed].nickname}\n"

            self._active_role = None
            self._time = "day"
            self.send_message("\nGOOD MORNING\n")
            self.send_message(dead_list)
            if count["mafia"] >= count["citizen"] + count["policeman"] or count["mafia"] == 0:
                self.set_default()
                break
            self.send_message("IT'S TIME TO DECIDE")
            time.sleep(wait_all)
            executed = None
            if self._voting:
                v = Counter(self._voting)
                executed = list(v.keys())[0]
                self._voting = []
                self._voted = []
            if executed:
                if self.members[executed].status == "alive":
                    role = self.members[executed].role
                    self.members[executed].dead()
                    count[role] -= 1
                    self.send_message(f"{self.members[executed].nickname} WAS EXECUTED")
            else:
                self.send_message("VOTING WAS SKIPPED")
        if count["mafia"]:
            self.send_message("\nMAFIA WON!\n")
        else:
            self.send_message("\nCITIZENS WON!\n")
        self.set_default()



if __name__ == '__main__':
    port = config.PORT
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rpc.add_GameServerServicer_to_server(GameServer(config.PLAYERS_COUNT), server)
    print('Starting server. Listening...')
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    server.wait_for_termination()
