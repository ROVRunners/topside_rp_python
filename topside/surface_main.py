"""Main file for the surface station."""
import time
from typing import Callable

import enums
import rov
import rov_config

import controller_input
import mqtt_handler
import socket_handler
import terminal_listener
from controller import Controller


class MainSystem:
    """Main class for the surface station system."""

    _rov: rov.ROV

    def __init__(self) -> None:
        """Initialize an instance of the class"""
        self.run = True

        # Set the number of loops per second and the number of nanoseconds per loop for rate limiting.
        self._loops_per_second = 60
        self._nanoseconds_per_loop = 1_000_000_000 // self._loops_per_second

        # Set up the configuration for the ROV.
        self.rov_config = rov_config.ROVConfig()

        # Get the communications interface information.
        self._video_port = self.rov_config.video_port
        self._comms_port = self.rov_config.comms_port
        self._host_ip = self.rov_config.host_ip

        # TODO: Set this up to receive the video stream(s)
        # self.socket = socket_handler.SocketHandler(self, self.pi_ip, self.video_port)

        # Set up the
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
        self._io = IO(self.input_handler, self.rov_connection)
        self._rov = rov.ROV(self.rov_config, self._io)

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


class IO:
    """Handles the input and output of the custom control classes."""
    def __init__(
            self,
            input_handler: controller_input.InputHandler | None = None,
            rov_comms: mqtt_handler.ROVConnection | None = None,
            terminal: terminal_listener.TerminalListener | None = None,
            rov_video: socket_handler.SocketHandler | None = None,
            ) -> None:
        """Initialize an instance of the class."""
        self._input_handler = input_handler
        self._rov_comms = rov_comms
        self._terminal = terminal
        self._rov_video = rov_video

        self._input_list = self._input_handler.get_inputs()
        self._subscriptions = self._rov_comms.get_subscriptions()
        self._video = self._rov_video.get_frame()

    @property
    def input_handler(self) -> controller_input.InputHandler:
        return self._input_handler

    @property
    def rov_comms(self) -> mqtt_handler.ROVConnection:
        return self._rov_comms

    @property
    def terminal(self) -> terminal_listener.TerminalListener:
        return self._terminal

    @property
    def rov_video(self) -> socket_handler.SocketHandler:
        return self._rov_video

    @property
    def input_list(self) -> dict[enums.ControllerNames, Controller]:
        return self._input_list

    @property
    def controller_inputs(self) -> dict[str, any]:
        """Get the controller inputs."""
        return self._input_handler.get_inputs()

    @property
    def subscriptions(self) -> dict[str, any]:
        """Get the subscriptions."""
        return self._rov_comms.get_subscriptions()

    def get_inputs(self) -> dict[str, any]:
        """Get the inputs from the input handler."""
        return self._input_list

    def get_subscriptions(self) -> dict[str, any]:
        """Get the subscriptions from the ROV connection."""
        return self._rov_comms.get_subscriptions()

    def get_video(self) -> any:
        """Get the video stream from the Raspberry Pi."""
        return self._rov_video.get_video()

    def start_listening(self) -> None:
        """Start listening for terminal input."""
        self._terminal.start_listening()

    def update_inputs(self) -> None:
        """This should be called only from rov.py. Do not call more than once per frame.

    def shutdown(self) -> None:
        """Shut down the IO system."""
        self._terminal.stop_listening()
        self._rov_video.shutdown()
        self._rov_comms.shutdown()
