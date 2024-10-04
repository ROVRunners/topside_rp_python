import thruster_pwm


class Manual:
    """The manual class for the spike."""

    def __init__(self, main_system):
        """Initialize the Manual object.

        Args:
            main_system (MainSystem):
                The main system object.
        """
        self.main_system = main_system

        self.sensor_data = {}
        self.controller_data = {}
        self.terminal_data = {}
        self.pwm_values = []

        # Add whatever you need initialized here.

    def manual_intercepts(self, controller_data, terminal_data, sensor_data, cv_frame=None):
        """Intercept the data from the controller, terminal, and sensor data.

        Args:
            controller_data (dict):
                The data from the controller.
            terminal_data (dict):
                The data from the terminal.
            sensor_data (dict):
                The data from the sensors.
            cv_frame (numpy.ndarray, optional):
                The OpenCV frame.

        Returns: terminal_data, display_cv_frame, pwm_values
        """
        # Data formats:
        # controller_data = {
        #     "FORWARD/BACKWARD": 0.5,
        #     "LEFT/RIGHT": 0.0,
        #     "UP/DOWN": 1.0,
        #     "YAW": 0.0,
        #     "PITCH": 0.0,
        #     "ROLL": 0.0,
        #     "HALT": 0.0,
        #     "CUSTOM_BUTTON_1": 0.0,
        #     "CUSTOM_BUTTON_2": 1.0,
        #     "CUSTOM_BUTTON_3": 0.0,
        # }
        # terminal_data = {
        #     "command": "command",
        #     "args": ["arg1", "arg2"], # Optional, space-separated arguments.
        # }
        # sensor_data = {
        #     "original_command": "", # Optional, the original command, not yet implemented
        #     "response": "",
        #     "clock_ms": [time.time_ns() / 1_000_000],
        #     "sensor1": [0],
        #     "sensor2": [5],
        #     "sensor3": [32],
        # }

        # Commands
        commands = []

        self.sensor_data = sensor_data | {}
        self.controller_data = controller_data | {}
        self.terminal_data = terminal_data + ""

        # Add your custom pwm conversion and any PID logic here.
        self.pwm_values = thruster_pwm.get_pwm_values(controller_data["FORWARD/BACKWARD"],
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
        # elif controller_data["CUSTOM_BUTTON_1"] == 1.0:
        #     commands.append("custom_button_1")
        #     # Custom button 1 logic here

        return controller_data, terminal_data, self.sensor_data, self.pwm_values

    def terminal_intercepts(self):
        """Intercept the terminal data."""
        # Data formats:
        # terminal_data = {
        #     "command": "command",
        #     "args": ["arg1", "arg2"], # Optional, space-separated arguments.
        # }

        # Add your custom terminal commands here.
        if self.terminal_data == "custom_command":
            # Custom command logic here
            pass
        elif self.terminal_data == "quit":
            self.main_system.shutdown()
