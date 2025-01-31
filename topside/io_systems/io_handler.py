import controller
import controller_input
from io_systems import gpio_handler, i2c_handler, mqtt_handler, terminal_listener, socket_handler, udp_socket
import enums
import utilities.class_tools as class_tools

class IO:
    """Handles the input and output of the custom control classes."""
    def __init__(
            self,
            gpio: gpio_handler.GPIOHandler,
            i2c: i2c_handler.I2CHandler,
            input_handler: controller_input.InputHandler | None = None,
            rov_comms: mqtt_handler.ROVConnection | None = None,
            terminal: terminal_listener.TerminalListener | None = None,
            rov_video: udp_socket.UDPSocket | None = None
            ) -> None:
        """Initialize an instance of the class."""
        self._input_handler = input_handler
        self._rov_comms = rov_comms
        self._terminal = terminal
        self._rov_video = rov_video
        self._i2c_handler = i2c
        self._gpio_handler = gpio

        self._controller_inputs = self._input_handler.controllers
        self._subscriptions = self._rov_comms.get_subscriptions()
        self._input_handler.update()
        # TODO: Hook up the UDP stuff
        # self._video = self._rov_video.get_frame()
        self._timer = class_tools.Stopwatch()

        self._mavlink_msg_requests: dict[int, int] = {}  # msg_id: interval

    @property
    def controllers(self) -> dict[enums.ControllerNames, controller.Controller]:
        """Get the controller inputs."""
        return self._input_handler.controllers

    @property
    def subscriptions(self) -> dict[str, any]:
        """Get the subscriptions."""
        return self._subscriptions

    @property
    def gpio_handler(self) -> gpio_handler.GPIOHandler:
        return self._gpio_handler

    @property
    def i2c_handler(self) -> i2c_handler.I2CHandler:
        return self._i2c_handler

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
    def rov_video(self) -> socket_handler.SocketHandler | None:
        # return self._rov_video
        return

    @property
    def timer(self) -> class_tools.Stopwatch:
        return self._timer

    # def get_video(self) -> any:
    #     """Get the video stream from the Raspberry Pi."""
    #     return self._rov_video.get_video()

    def start_listening(self) -> None:
        """Start listening for terminal input."""
        self._rov_comms.connect()
        self._terminal.start_listening()
        # self._rov_video.start_listening()

    def update(self) -> None:
        """This should be called only from rov.py. Do not call more than once per frame."""
        self._input_handler.update()
        self._subscriptions = self.rov_comms.get_subscriptions()
        self._gpio_handler.update(self._subscriptions)
        self._i2c_handler.update(self._subscriptions)
        self._rov_comms.publish_i2c(self.i2c_handler.i2cs)
        self._rov_comms.publish_pins(self._gpio_handler.pins)
        self._rov_comms.publish_mavlink_data_request(self._mavlink_msg_requests)

    def shutdown(self) -> None:
        """Shut down the IO system gracefully."""
        self._terminal.stop_listening()
        # self._rov_video.shutdown()
        self._rov_comms.shutdown()
        self._input_handler.shutdown()

    def add_mavlink_subscription(self, msg_id: int, interval: int = 1_000_000) -> None:
        """Add a mavlink subscription."""
        self._mavlink_msg_requests[msg_id] = interval
