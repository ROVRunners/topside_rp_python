"""Main file for the surface station."""
import os
import sys
import time
from typing import Callable

import socket_handler
import controller_input
import mqtt_handler

import rovs.spike.rov as rov
import rovs.spike.rov_config as rov_config


class MainSystem:
    """Main class for the surface station system."""

    _rov: rov.ROV

    def __init__(self) -> None:
        """Initialize an instance of the class"""
        self.run = True

        # Set the number of loops per second and the number of nanoseconds per loop for rate limiting.
        self._loops_per_second = 60
        self._nanoseconds_per_loop = 1_000_000_000 // self._loops_per_second

################################################################
        """change which ROV is used here"""  # TODO: No.
        self.rov_config = rov_config.ROVConfig()
################################################################

        self.video_port = self.rov_config.video_port
        self.comms_port = self.rov_config.comms_port
        self.host_ip = self.rov_config.host_ip

        # TODO: Set this up to receive the video stream(s)
        # self.socket = socket_handler.SocketHandler(self, self.pi_ip, self.video_port)

        self.controller = controller_input.Controller(self.rov_config.controller_config)

        # The MQTT handler is used to communicate with the ROV sending and receiving thruster commands and sensor data.
        self.rov_connection = mqtt_handler.ROVConnection(self.host_ip, self.comms_port)

        # TODO: Incorporate terminal input and openCV video stream(s). Maybe incorporate a video stream switching
        #  system.
        self.input_map: dict[str, Callable[[], any]] = {
            "controller": self.controller.get_inputs,
            "subscriptions": self.rov_connection.get_subscriptions,
        }
        # TODO: Create an output map for the Manual class to access mqtt and other functions.

        self._rov = rov.ROV(self.rov_config, self.input_map, self.rov_connection)

        self.rov_connection.connect()

        # self.socket.connect_outbound()
        # self.socket.start_listening()
        # self.terminal.start_listening()

    def main_loop(self) -> None:
        """Executes the main loop of the program."""
        # Get the time at the start of the loop.
        start_loop: int = time.monotonic_ns()

        # Execute the loop of the ROV.
        self._rov.run()

        # Rate limit the loop to the specified number of loops per second.
        end_loop: int = time.monotonic_ns()
        loop_time: int = end_loop - start_loop
        sleep_time: float = (self._nanoseconds_per_loop - loop_time) / 1_000_000_000
        if sleep_time > 0:
            time.sleep(sleep_time)
            # print(sleep_time)

    def shutdown(self) -> None:
        """Shuts down the system and its subsystems."""
        self.run = False
        self._rov.shutdown()
        self.rov_connection.shutdown()
        # self.socket.shutdown()
        # Delay to let things close properly
        time.sleep(.25)


