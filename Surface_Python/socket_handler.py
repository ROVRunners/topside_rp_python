"""Socket handler for the surface system."""

# pylint: disable=wildcard-import, unused-import, unused-wildcard-import

import socket
import threading
from time import sleep
from utilities.personal_functions import *


class SocketHandler:
    """Class for handling socket communication with the Raspberry Pi."""

    def __init__(self, main_system, ip_address: str, port: str = "5600", timeout: float = .25,
                 max_attempts: int = 40, buffer_size: int = 1024, encoding: str = 'utf-8') -> None:
        """Initialize the SocketHandler object.

        Args:
            main_system (object):
                The main system object.
            ip_address (str):
                The IP address to connect to.
            port (int, optional):
                The port number to connect to. Defaults to "5600".
            timeout (float, optional):
                The timeout value for socket operations. Defaults to 0.25.
            max_attempts (int, optional):
                The maximum number of connection attempts. Defaults to 40.
            buffer_size (int, optional):
                The size of the receive buffer. Defaults to 1024.
            encoding (str, optional):
                The encoding to use for data transmission. Defaults to 'utf-8'.
        """
        self.main_system = main_system
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.buffer_size = buffer_size
        self.encoding = encoding

        self.lock = threading.Lock()
        self.message_buffer = []

        self.setup_socket()

    def setup_socket(self) -> None:
        """Set up a socket connection with the specified IP address and port.

        Raises:
            ConnectionRefusedError:
                If the connection is refused after the maximum number of attempts.
        """
        attempts = 0
        while True:
            attempts += 1
            try:
                # Try to connect and break out of the loop upon a successful connection.
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.ip_address, self.port))
                break
            except ConnectionRefusedError:
                # If it hasn't connected after {attempts} attempts,
                # (default 40 @ .25s intervals), give up.
                if attempts > self.max_attempts:
                    error("Connection refused. Exiting...")
                    self.main_system.shutdown()

                error("Connection refused. Retrying...")
                sleep(self.timeout)

    def send_packet(self, command: str, pwm_values: list[int]) -> None:
        """Send a packet to the Raspberry Pi with the specified command and PWM values.
        
        Args:
            command (str):
                The command to send to the Raspberry Pi.
            pwm_values (list[int]):
                A list of PWM values to send to the Raspberry Pi.
        """
        try:
            # Create and send the packet.
            packet_data = f"{command}|[]|{','.join(map(str, pwm_values))}"
            self.sock.sendall(packet_data.encode(self.encoding))

            # Wait for the response.
            response = self.sock.recv(self.buffer_size)
            print(f"Received response: {response.decode()}")
        except ConnectionResetError:
            # If the connection is reset, attempt to reconnect.
            print("Connection reset. Reconnecting...")
            self.setup_socket()

    def shutdown(self) -> None:
        """Close the socket connection."""
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
