import enum
import time

from enums import MavlinkMessageTypes


class MavlinkHandler:
    
    mavlink_commands: dict[MavlinkMessageTypes, tuple[int, int, int, int, int, int, int]]  # dict[message_type, tuple[param1, param2, param3, param4, param5, param6, param7]]
    mavlink_messages: dict[str, dict]
    # _last_mavlink_commands: dict[MavlinkMessageTypes, tuple[int, int, int, int, int, int, int]]

    def __init__(self):

        self.mavlink_commands = {}  # commands that will be sent to mavlink
        self.mavlink_messages = {}  # received data from mavlink
        # self._last_mavlink_commands = {}

    def update(self, subs: dict[str, dict]) -> None:
        for i in subs.keys():
            if i.startswith("ROV/mavlink/"):
                name = i.split("/")[2]

                self.mavlink_messages[name] = subs[i]
    
    def add_command(self, command: MavlinkMessageTypes, parameters: tuple[int, int, int, int, int, int, int]):
        self.mavlink_commands[command] = parameters
    
    @property
    def mavlink_commands(self):
        return self.mavlink_commands
    
    @mavlink_commands.setter
    def mavlink_commands(self, mavlink_commands: dict[MavlinkMessageTypes, tuple[int, int, int, int, int, int, int]]):
        self.mavlink_commands = mavlink_commands
    
