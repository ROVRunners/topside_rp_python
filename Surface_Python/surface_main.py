"""Main file for the surface station."""

# pylint: disable=wildcard-import, unused-import, unused-wildcard-import
import os
import sys
import argparse
from time import sleep

# import terminal_listener
import socket_handler
import controller_input


utilities_directory = os.path.dirname(os.path.realpath(__file__))
utilities_directory = os.path.join(utilities_directory, "utilities")
sys.path.append(utilities_directory)


rov_config_directory = os.path.dirname(os.path.realpath(__file__))
rov_config_directory = os.path.join(rov_config_directory, "rov_config")
sys.path.append(rov_config_directory)

# from spike import rov_config

from personal_functions import *

DEFAULT_IP = "169.254.5.24"
DEFAULT_PORT = 5600
DEFAULT_ROV = "spike"


class MainSystem:
    """Main class for the surface station system."""

    def __init__(self, pi_ip, pi_port, rov_dir: str) -> None:
        """Initialize an instance of the class.

        Args:
            pi_ip (str):
                The IP address of the Raspberry Pi.
            pi_port (int):
                The port number to use for the socket connection.
            rov_dir (str):
                The directory containing the ROV configuration files.
        """
        self.run = True

        self.pi_ip = pi_ip
        self.pi_port = pi_port

        # self.terminal = terminal_listener.TerminalListener(self)
        self.socket = socket_handler.SocketHandler(self, self.pi_ip, self.pi_port)
        self.controller = controller_input.Controller(rov_dir)
        self.ROV = rov_config.ROVConfig()
        self.man_class = self.ROV.manual_class(self)

        self.safe_pwm_values = self.ROV.stationary_pwm_values

        self.socket.connect_outbound()
        # self.socket.start_listening()
        # self.terminal.start_listening()

        self.sensor_data = {}
        self.inputs = {}
        self.command = ""
        self.pwm_values = self.safe_pwm_values
        self.pi_commands = []

    def main_loop(self) -> None:
        """Executes the main loop of the program."""
        # Get controller inputs
        self.inputs = self.controller.get_controller_commands()
        print(self.inputs)

        # Get sensor data from previous loop returns.
        if self.socket.sensor_data_available:
            self.sensor_data = self.socket.get_sensor_data()
        else:
            self.sensor_data = {}
        print("Sensor data:", self.sensor_data)

        # Check for terminal input
        # if self.terminal.check_for_input():
        #     self.command = self.terminal.get_input_value()
        #     print("Command: " + self.command)
        self.command = ""

        # Hand off for modification and custom commands

        # Handle commands

        # Convert controls to PWM signals
        # self.pwm_values = self.ROV.pwm_conversion_function(self.inputs["FORWARD/BACKWARD"],
        #                                                    self.inputs["LEFT/RIGHT"],
        #                                                    self.inputs["UP/DOWN"],
        #                                                    self.inputs["YAW"],
        #                                                    self.inputs["PITCH"],
        #                                                    0)
        self.inputs, self.command, self.sensor_data, self.pwm_values = (self.man_class.manual_intercepts(controller_data=self.inputs, terminal_data=self.command, sensor_data=self.sensor_data))

        print("Data modified by manual_intercepts:", self.inputs, self.command, self.sensor_data, self.pwm_values)
        # Send data to the Raspberry Pi
        self.socket.send_commands(self.pi_commands, self.pwm_values)
        print("Sent data to Raspberry Pi:", self.pi_commands, self.pwm_values)
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
    ap.add_argument("-r", "--rov", type=str, required=False,
                    help="the name of the folder containing the rov configuration files")
    args = vars(ap.parse_args())
    ip = None
    port = None
    rov = None
    if args["ip"] is None:
        ip = intext("Please provide the IP address of the Raspberry Pi. " +
                    f"Defaults to \"{DEFAULT_IP}\"").strip()
        if ip == "":
            ip = DEFAULT_IP
    if args["ip"] is None:
        port = intext("Please provide the port you want to use. " +
                      f"Defaults to {DEFAULT_PORT}").strip()
        if port == "":
            port = DEFAULT_PORT
        port = int(port)
    if args["rov"] is None:
        rov = intext("Please provide the rov you want to use. " +
                     f"Defaults to {DEFAULT_ROV}").strip()
        if rov == "":
            rov = DEFAULT_ROV

    rov_directory: str = os.path.join(rov_config_directory, rov)
    sys.path.append(rov_directory)

    import rov_config

    main_system = MainSystem(ip, port, rov_directory)

    while main_system.run:
        main_system.main_loop()
