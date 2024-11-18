"""Main file for the surface station."""
import os
import sys
import time
from typing import Callable

import terminal_listener
import socket_handler
import controller_input

# from rovs.spike import Spike, SpikeConfig
import rovs.spike.rov as rov
import rovs.spike.rov_config as rov_config


class MainSystem:
    """Main class for the surface station system."""

    _rov: rov.Spike  # TODO: This should be changeable to any ROV type, currently there is only Spike

    def __init__(self) -> None:
        """Initialize an instance of the class"""
        self.run = True

################################################################
        """change which ROV is used here"""
        self.rov_config = SpikeConfig()
################################################################

        self.pi_ip = self.rov_config.ip
        self.pi_port = self.rov_config.port
        self.rov_dir = self.rov_config.rov

        self.terminal = terminal_listener.TerminalListener(self)
        self.socket = socket_handler.SocketHandler(self, self.pi_ip, self.pi_port)

        self.controller = controller_input.Controller(self.rov_config.controller_config, self.rov_dir)

        self.input_map: dict[str, Callable[[], any]] = {
            "controller": self.controller.get_inputs,
        }

        self._rov = rov.Spike(self.rov_config, self.input_map)

        # self.safe_pwm_values = self.ROV.stationary_pwm_values

        # self.socket.connect_outbound()
        # self.socket.start_listening()
        # self.terminal.start_listening()

        self.sensor_data = {}
        self.inputs = {}
        self.command = ""
        # self.pwm_values = self.safe_pwm_values
        self.pi_commands = []

    def main_loop(self) -> None:
        """Executes the main loop of the program."""
        # Get controller inputs
        # self.inputs = self.controller.get_controller_commands()
        # print(self.inputs)

        self._rov.run()

        # Get sensor data from previous loop returns.
        if self.socket.sensor_data_available:
            self.sensor_data = self.socket.get_sensor_data()

        # Check for terminal input
        # if self.terminal.check_for_input():
        #     self.command = self.terminal.get_input_value()
        #     print("Command: " + self.command)

        # Hand off for modification and custom commands

        # Handle commands

        # Convert controls to PWM signals
        # self.pwm_values = self.ROV.pwm_conversion_function(self.inputs["FORWARD/BACKWARD"],
        #                                                    self.inputs["LEFT/RIGHT"],
        #                                                    self.inputs["UP/DOWN"],
        #                                                    self.inputs["YAW"],
        #                                                    self.inputs["PITCH"],
        #                                                    0)
        #
        # # Send data to the Raspberry Pi
        # self.socket.send_commands(self.pi_commands, self.pwm_values)

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
        """Shuts down the system and its subsystems."""

        self.run = False
        # Delay to let things close properly
        time.sleep(1)

        self.socket.shutdown()
        sys.exit()

