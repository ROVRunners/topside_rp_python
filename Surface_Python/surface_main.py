"""Main file for the surface station."""

# pylint: disable=wildcard-import, unused-import, unused-wildcard-import

import argparse
import sys
import terminal_listener
import socket_handler
from utilities.personal_functions import *

default_ip = "192.168.1.2"
default_port = "5600"

class MainSystem:
    """Main class for the surface station system."""

    def __init__(self, pi_ip, port: str="5600") -> None:
        """Initialize an instance of the class.

        Args:
            pi_ip (str):
                The IP address of the Raspberry Pi.
            port (str, optional):
                The port number to use for the socket connection.
                Defaults to "5600".
        """
        self.terminal = terminal_listener.TerminalListener(self)
        self.packet_sender = socket_handler.SocketHandler(self, pi_ip, port)
        self.run = True


    def main_loop(self) -> None:
        pass
        # read_input()



    def shutdown(self) -> None:
        sys.exit()


if __name__ == '__main__':
    # Construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars( ap.parse_args() )

    if args["ip"] is None:
        ip = intext("Please provide the IP address of the Raspberry Pi." +
                    f"Defaults to \"{default_ip}\"").strip()
        if ip == "":
            ip = default_ip
    if args["ip"] is None:
        port = intext("Please provide the port you want to use." +
                      f"Defaults to \"{default_port}\"").strip()
        if port == "":
            port = default_port

    main_system = MainSystem(ip, port)
