from hardware import thruster_pwm
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish


class Manual:
    """The manual control class for the spike."""
    @property
    def inputs(self):
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def __init__(self, frame: thruster_pwm.FrameThrusters):
        """Initialize the Manual object.

        Args:
            frame (thruster_pwm.FrameThrusters):
                The objects of the thrusters mounted to the frame.
        """

        self._frame = frame

        # self.sensor_data = {}
        # self.controller_data = {}
        # self.terminal_data = {}
        # self.pwm_values = []

        # Add whatever you need initialized here.

    def update(self, inputs: dict[str, any]):
        self.pwm_values = self._frame.get_pwm_values(inputs["FORWARD/BACKWARD"],
                                                     inputs["LEFT/RIGHT"],
                                                     inputs["UP/DOWN"],
                                                     inputs["YAW"],
                                                     inputs["PITCH"],
                                                     0)
        # publish.single("thruster_pwm", self.pwm_values, hostname="localhost")


    def manual_intercepts(self, controller_data, terminal_data, sensor_data, cv_frame):
        """Intercept the data from the controller, terminal, and sensor data.

        Args:
            controller_data (dict):
                The data from the controller.
            terminal_data (dict):
                The data from the terminal.
            sensor_data (dict):
                The data from the sensors.
            cv_frame (numpy.ndarray):
                The OpenCV frame.

        Returns: terminal_data, display_cv_frame, pwm_values
        """


        # Commands
        commands = []

        self.sensor_data = sensor_data | {}
        self.controller_data = controller_data | {}
        self.terminal_data = terminal_data | {}

        # Add your custom pwm conversion and any PID logic here.
        self.pwm_values = self._frame.get_pwm_values(controller_data["FORWARD/BACKWARD"],
                                                      controller_data["LEFT/RIGHT"],
                                                      controller_data["UP/DOWN"],
                                                      controller_data["YAW"],
                                                      controller_data["PITCH"],
                                                      0)

        # Create custom terminal commands
        self.terminal_intercepts()

        # Run custom controller button commands.
        if controller_data["HALT"] == 1.0:
            self.pwm_values = self.main_system.safe_pwm_values
            # Do whatever else you need to do here to halt the ROV.
        elif controller_data["CUSTOM_BUTTON_1"] == 1.0:
            commands.append("custom_button_1")
            # Custom button 1 logic here

        return controller_data, terminal_data, sensor_data, self.pwm_values

    def terminal_intercepts(self):
        """Intercept the terminal data."""
        # Data formats:
        # terminal_data = {
        #     "command": "command",
        #     "args": ["arg1", "arg2"], # Optional, space-separated arguments.
        # }

        # Add your custom terminal commands here.
        if self.terminal_data["command"] == "custom_command":
            # Custom command logic here
            pass
        elif self.terminal_data["command"] == "quit":
            self.main_system.shutdown()
