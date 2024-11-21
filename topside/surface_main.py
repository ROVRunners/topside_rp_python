"""Main file for the surface station."""
import time
from typing import Callable

import hardware.rov as rov
import rov_config

import controller_input
import mqtt_handler


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

        self._video_port = self.rov_config.video_port
        self._comms_port = self.rov_config.comms_port
        self._host_ip = self.rov_config.host_ip

        # TODO: Set this up to receive the video stream(s)
        # self.socket = socket_handler.SocketHandler(self, self.pi_ip, self.video_port)

        self.input_handler = controller_input.InputHandler(self.rov_config.controllers)

        # The MQTT handler is used to communicate with the ROV sending and receiving thruster commands and sensor data.
        self.rov_connection = mqtt_handler.ROVConnection(self._host_ip, self._comms_port)

        # TODO: Incorporate terminal input and openCV video stream(s). Maybe incorporate a video stream switching
        #  system.
        self.input_map: dict[str, Callable[[], any]] = {
            "controller": self.input_handler.get_inputs,
            "subscriptions": self.rov_connection.get_subscriptions,
            # "socket": self.socket.get_video,
        }

        self._rov = rov.ROV(self)

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

    def shutdown(self) -> None:
        """Shuts down the system and its subsystems."""
        self.run = False
        self._rov.shutdown()
        self.rov_connection.shutdown()
        # self.socket.shutdown()
        # Delay to let things close properly
        time.sleep(.25)
