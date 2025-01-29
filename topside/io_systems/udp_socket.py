"""Socket video communications handler for the surface system."""
from config.video import VideoConfig
import socket
import cv2
import numpy as np


class UDPSocket:

    def __init__(self, config: VideoConfig):
        self._config = config

        self._ip = self._config.ip_address
        self._port = self._config.port

        self.delimiter = b'FRAME_END_MARKER'
        self.chunk_size = self._config.chunk_size
        self._width = self._config.width
        self._height = self._config.height

    def run(self):

        try:  # Create the UDP socket
            self.UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.UDP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self._config.buffer_size)

            # Bind the socket to listen for incoming video stream
            self.UDP_socket.bind((self._ip, self._port))
            print(f"UDP socket bound to {self._ip}:{self._port}")

            # Create a window for displaying video
            cv2.namedWindow("Received Video Feed", cv2.WINDOW_NORMAL)

            while True:
                # Buffer to store received frame chunks
                frame_data = bytearray()

                while True:
                    # Receive chunks of the video stream
                    chunk, addr = self.UDP_socket.recvfrom(self.chunk_size)
                    if chunk == self.delimiter:
                        print("End of frame received")
                        break  # End of current frame, exit the loop

                    # Append chunk to the frame data buffer
                    frame_data.extend(chunk)

                # Decode the frame data into an image
                frame = cv2.imdecode(np.frombuffer(frame_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                # If frame is valid, display it
                if frame is not None:
                    frame = cv2.resize(frame, (self._width, self._height))
                    cv2.imshow("Received Video Feed", frame)

                # Exit condition: press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            print("Closing the socket and cleaning up.")
            self.UDP_socket.close()
            cv2.destroyAllWindows()
