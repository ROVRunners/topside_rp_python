"""Socket video communications handler for the surface system."""


class SocketHandler:
    """Class for handling socket communication with the Raspberry Pi."""

    def __init__(self):
        """Initialize the SocketHandler object."""
        pass

    def start_listening(self):
        """Await a connection attempt from the Raspberry Pi."""
        pass

    def get_video(self):
        """Get the video stream from the Raspberry Pi."""
        pass

    def get_frame(self):
        """Get the frame from the Raspberry Pi."""
        pass

    def shutdown(self):
        """Close the socket connection."""
        pass


# """Socket handler for the surface system."""
# import json
# # pylint: disable=wildcard-import, unused-import, unused-wildcard-import
#
# import socket
# import threading
# import time
#
# # from utilities.personal_functions import *
#
#
# class SocketHandler:
#     """Class for handling socket communication with the Raspberry Pi."""
#
#     def __init__(self, main_system, ip_address: str, port: int = 5600, timeout: float = .25,
#                  max_attempts: int = 40, buffer_size: int = 1024, encoding: str = 'utf-8') -> None:
#         """Initialize the SocketHandler object.
#
#         Args:
#             main_system (MainSystem):
#                 The main system object.
#             ip_address (str):
#                 The IP address to connect to.
#             port (int, optional):
#                 The port number to connect to.
#                 Defaults to 5600.
#             timeout (float, optional):
#                 The timeout value for socket operations.
#                 Defaults to 0.25.
#             max_attempts (int, optional):
#                 The maximum number of connection attempts.
#                 Defaults to 40.
#             buffer_size (int, optional):
#                 The size of the reception buffer.
#                 Defaults to 1024.
#             encoding (str, optional):
#                 The encoding to use for data transmission.
#                 Defaults to 'utf-8'.
#         """
#         self.main_system = main_system
#         self.ip_address: str = ip_address
#         self.port: int = port
#         self.timeout: float = timeout
#         self.max_attempts: int = max_attempts
#         self.buffer_size: int = buffer_size
#         self.encoding: str = encoding
#
#         # self.lock: threading.Lock = threading.Lock()
#         self.sensor_data: dict[str, list] = {}
#         self.sensor_data_available: bool = False
#
#         self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
#     def _setup_socket(self) -> None:
#         """Set up a socket connection with the specified IP address and port.
#
#         Raises:
#             ConnectionRefusedError:
#                 If the connection is refused after the maximum number of attempts.
#         """
#         attempts: int = 0
#         while True:
#             attempts += 1
#             try:
#                 # Try to connect and break out of the loop upon a successful connection.
#                 print(f"Trying to connect to {self.ip_address}:{self.port}...")
#                 self.socket.connect((self.ip_address, self.port))
#                 print(f"Connected outbound to {self.ip_address}:{self.port}")
#
#                 print("Pinging Raspberry Pi...")
#                 start_ping = time.time_ns()
#                 self.socket.send(json.dumps({
#                     "commands": ["ping"],
#                     "pwm_values": self.main_system.safe_pwm_values
#                 }).encode(self.encoding))
#
#                 pong_maybe = json.loads(self.socket.recv(self.buffer_size).decode(self.encoding))
#                 end_ping = time.time_ns()
#                 print(pong_maybe["response"])
#                 print(f"Ping time: {(end_ping - start_ping) / 1_000_000}ms")
#
#                 break
#             except (ConnectionRefusedError, TimeoutError):
#                 # If it hasn't connected after {attempts} attempts, give up.
#                 if attempts > self.max_attempts:
#                     print("Outbound connection refused too many times. Exiting...")
#                     self.main_system.shutdown()
#
#                 print(f"Outbound connection refused ({attempts}). Retrying...")
#                 time.sleep(self.timeout)
#
#     # def start_listening(self) -> None:
#     #     """Start listening for input in a separate thread."""
#     #     threading.Thread(target=self._listen_for_data).start()
#
#     def connect_outbound(self) -> None:
#         """Connect to the Raspberry Pi."""
#         print("Initializing socket handler...")
#         self._setup_socket()
#
#     # def _listen_for_data(self) -> None:
#     #
#     #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     #
#     #         host: str = "0.0.0.0"
#     #
#     #         while self.main_system.run:
#     #
#     #             server_socket.bind((host, self.port))
#     #             server_socket.listen()
#     #             text(f"Server listening on {host}:{self.port}")
#     #
#     #             client_socket, client_address = server_socket.accept()
#     #             text(f"Accepted connection from {client_address}")
#     #
#     #             try:
#     #                 while True:
#     #                     # Receive data from the socket.
#     #                     data_bytes: bytes = server_socket.recv(self.buffer_size)
#     #                     if not data_bytes:
#     #                         continue
#     #
#     #                     # Decode the data.
#     #                     data = json.loads(data_bytes)
#     #
#     #                     # Set the data var to the packets.
#     #                     with self.lock:
#     #                         self.sensor_data = data
#     #                         self.sensor_data_available = True
#     #
#     #             except ConnectionResetError:
#     #                 print("Inbound connection reset. Reconnecting...")
#     #
#     #         server_socket.close()
#
#     def send_commands(self, commands: list[str], pwm_values: list[int]) -> None:
#         """Send a packet to the Raspberry Pi with the specified commands and PWM values.
#
#         Args:
#             commands (list[str]):
#                 The command to send to the Raspberry Pi.
#             pwm_values (list[int]):
#                 A list of PWM values to send to the Raspberry Pi.
#         """
#         try:
#             # Create and send the packet.
#             packet_data: dict[str, list] = {
#                 "commands": commands,
#                 "pwm_values": pwm_values
#             }
#             encoded_packet_data: bytes = json.dumps(packet_data).encode(self.encoding)
#             self.socket.sendall(encoded_packet_data)
#
#             # Wait for the response.
#             response: bytes = self.socket.recv(self.buffer_size)
#             print(f"Received response: {json.loads(response.decode(self.encoding))}")
#
#         except ConnectionResetError:
#             # If the connection is reset, attempt to reconnect.
#             print("Connection reset. Reconnecting...")
#             self._setup_socket()
#
#     def get_sensor_data(self) -> dict[str, list | str]:
#         """Get the sensor data from the Raspberry Pi.
#
#         Returns:
#             dict[str, list | str]: The sensor data with the key as the sensor name.
#         """
#         # with self.lock:
#         #     # Get the sensor data from the message buffer.
#         #     data = self.sensor_data
#         #     self.sensor_data = {}
#         #     self.sensor_data_available = False
#         #
#         # return data
#         return self.sensor_data
#
#     def shutdown(self) -> None:
#         """Close the socket connection."""
#         self.socket.shutdown(socket.SHUT_RDWR)
#         self.socket.close()
