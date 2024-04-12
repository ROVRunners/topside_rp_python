"""Main file for the surface station."""

# pylint: disable=wildcard-import, unused-import, unused-wildcard-import

import argparse

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
            pi_port (str, optional):
                The port number to use for the socket connection.
                Defaults to "5600".
        """
        self.pi_ip = pi_ip
        self.pi_port = pi_port

        self.terminal = terminal_listener.TerminalListener(self)
        self.socket = socket_handler.SocketHandler(self, self.pi_ip, self.pi_port)
        self.controller = controller_input.Controller(self)

        self.socket.start_listening()
        self.terminal.start_listening()

        self.sensor_data = {}
        self.inputs = {}
        self.command = ""

        self.run = True

    def main_loop(self) -> None:
        """Executes the main loop of the program."""
        # Get controller inputs
        self.inputs = self.controller.get_inputs()

        # Get sensor data
        if self.socket.sensor_data_available:
            self.sensor_data = self.socket.get_sensor_data()

        # Check for terminal input
        if self.terminal.check_for_input():
            self.command = self.terminal.get_input_value()

        # Hand off for modification

        # Handle commands

        # Convert controls to PWM signals

        # Send data to the Raspberry Pi
        # self.socket_handler.send_commands(data)

        # Display frames

        # example C++ code:
        # for (int i = 0; i < gun_state.num_input_pins; i++) {
        #   gun_state.input_state[i] = digitalRead(inputs[i]);
        #   gun_state.input_state_changed[i] = gun_state.input_state[i] != gun_state.prev_input_state[i];
        #   gun_state.prev_input_state[i] = gun_state.input_state[i];
        # }
        #
        # bool any_changed = false;
        #
        # for (int i = 0; i < num_inputs; i++) {
        #   if (gun_state.input_state_changed[i]) {
        #     (*device_state_functions[i])(gun_state.input_state[i]);
        #     any_changed = true;
        #   }
        # }

    def shutdown(self) -> None:
        """Shuts down the system and it's subsystems."""

        self.run = False
        # Delay to let things close properly
        sleep(1)

        self.socket.shutdown()
        sys.exit()


if __name__ == '__main__':
    # Construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=False,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=False,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())
    ip = None
    port = None
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
