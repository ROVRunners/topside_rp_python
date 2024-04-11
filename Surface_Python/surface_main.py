"""Main file for the surface station."""

# pylint: disable=wildcard-import, unused-import, unused-wildcard-import

import argparse
import sys

import terminal_listener
import socket_handler
import controller_input

from utilities.personal_functions import *

DEFAULT_IP = "192.168.1.2"
DEFAULT_PORT = "5600"


class MainSystem:
    """Main class for the surface station system."""

    def __init__(self, pi_ip, pi_port: str = "5600") -> None:
        """Initialize an instance of the class.

        Args:
            pi_ip (str):
                The IP address of the Raspberry Pi.
            port (str, optional):
                The port number to use for the socket connection.
                Defaults to "5600".
        """
        self.terminal = terminal_listener.TerminalListener(self)
        self.socket_handler = socket_handler.SocketHandler(self, pi_ip, pi_port)
        self.controller = controller_input.Controller(self)

        self.sensor_data = {}
        self.inputs = {}
        self.command_buffer = []

        self.run = True

    def main_loop(self) -> None:
        self.inputs = self.controller.get_inputs()
        # self.sensor_data = self.socket_handler.get_sensor_data()
        if self.terminal.check_for_input():
            self.command_buffer.append(self.terminal.get_input_value())
        # Hand off for modification
        # Handle commands
        # self.socket_handler.send_data(data)
        # Display frames

    def shutdown(self) -> None:
        self.socket_handler.shutdown()
        sys.exit()


if __name__ == '__main__':
    # Construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

    if args["ip"] is None:
        ip = intext("Please provide the IP address of the Raspberry Pi." +
                    f"Defaults to \"{DEFAULT_IP}\"").strip()
        if ip == "":
            ip = DEFAULT_IP
    if args["ip"] is None:
        port = intext("Please provide the port you want to use." +
                      f"Defaults to \"{DEFAULT_PORT}\"").strip()
        if port == "":
            port = DEFAULT_PORT

    main_system = MainSystem(ip, port)
