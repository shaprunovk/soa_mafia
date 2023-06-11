class ClientCommands:
    LEAVE = "/leave"
    MEMBERS = "/members"
    VERIFY = "/verify"
    KILL = "/kill"
    EXECUTE = "/execute"
    SKIP = "/skip"
    SELF = "/me"
    HELP = "/help"
    READY = "/ready"
    COMMANDS_LIST = "LIST OF COMMANDS:\n" \
                    "   /leave - to leave server\n" \
                    "   /members - list of members\n" \
                    "   /me - shows your character (only during game)\n" \
                    "   /ready - vote to start game\n" \
                    "   /kill - kill players " \
                    "(only during game, available for policeman and mafia during night)\n" \
                    "   /verify {player_id} - shows role of the player " \
                    "(only during game, available for policeman during night)\n" \
                    "   /execute {player_id} - votes for executing player " \
                    "(only during game, available for citizens during day)\n" \
                    "   /skip - votes for skipping day without executing " \
                    "(only during game, available for citizens during day)\n"


client_commands = ClientCommands()
