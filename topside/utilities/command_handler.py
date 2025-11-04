
from utilities.personal_functions import *


class CommandHandler:
    def __init__(self, main_system):
        self.main_system = main_system
        self.command = None
        self.args = None

        self.command_dict = {
            "exit": [self.main_system.shutdown, "exit -- Exit the program."],
            # "help": [self._help_command, "help [command] -- Display this help message or help about a command."],
        }

    def command_handler(self, command: str) -> None:
        """Handles the command passed to the system.

        Args:
            command (str):
                The command to handle.
        """
        self.command, self.args = command.split(" ")[0], command.split(" ")[1:]

        if self.command in self.command_dict:
            self.command_dict[self.command][0]()

        if self.command == "exit":
            self.main_system.shutdown()
        elif self.command == "help":
            print("Commands:")
            for key in self.command_dict:
                print(f"\t{self.command_dict[key][1]}")
        else:
            print("Invalid command. Type 'help' for a list of commands.")
