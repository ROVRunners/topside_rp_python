import hardware.thruster_pwm as thruster_pwm
import mqtt_handler
import enums
import controller_input
import surface_main


class Manual:
    """The manual control class for the ROV."""

    def __init__(self, frame: thruster_pwm.FrameThrusters, main_system: 'surface_main.MainSystem') -> None:
        """Initialize the Manual object.

        Args:
            frame (thruster_pwm.FrameThrusters):
                The objects of the thrusters mounted to the frame.
            main_system ('surface_main.MainSystem'):
                The MainSystem object.
        """
        self._frame = frame
        self._main_system: 'surface_main.MainSystem' = main_system

        # Set up the objects
        self._rov_connection: mqtt_handler.ROVConnection = self._main_system.rov_connection
        self._input_handler: controller_input.InputHandler = self._main_system.input_handler

        # self.sensor_data = {}
        # self.terminal_data = {}

        # Add whatever you need initialized here.

    @property
    def inputs(self):
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def loop(self):
        """Update thrust values, send commands, and more based on the inputs."""
        inputs = self._input_handler.get_inputs()
        toggled_inputs = self._input_handler.get_toggled_inputs()

        controller = inputs[enums.ControllerNames.PRIMARY_DRIVER]
        controller_toggles = toggled_inputs[enums.ControllerNames.PRIMARY_DRIVER]

        subscriptions = self._rov_connection.get_subscriptions()

        # Get the sensor data from the subscriptions if it exists.
        if "ROV/sensor_data" in subscriptions:
            sensor_data = subscriptions["ROV/sensor_data"]

        # Convert the triggers to a single value.
        right_trigger = controller[enums.ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller[enums.ControllerAxisNames.LEFT_TRIGGER]
        vertical = controller_input.combine_triggers(left_trigger, right_trigger)

        # Break down the sensor data into its components (more can be added as needed).
        # gyro: dict[str, float] = sensor_data["gyroscope"]
        # accel: dict[str, float] = sensor_data["accelerometer"]
        # depth: float = sensor_data["depth"]
        # leak: bool = sensor_data["leak"]

        # TODO: Add any other input processing software like a PID here. Also, a PID should probably be
        #  implemented in a separate class due to it being generally applicable to all ROVs.

        # Get the PWM values for the thrusters based on the controller inputs.
        pwm_values: dict[enums.ThrusterPositions, int] = self._frame.get_pwm_values(
            {
                enums.Directions.FORWARDS: controller[enums.ControllerAxisNames.LEFT_Y],
                enums.Directions.RIGHT: controller[enums.ControllerAxisNames.LEFT_X],
                enums.Directions.UP: vertical,
                enums.Directions.YAW: controller[enums.ControllerAxisNames.RIGHT_X],
                enums.Directions.PITCH: controller[enums.ControllerAxisNames.RIGHT_Y],
                enums.Directions.ROLL: 0,
            },
        )

        # Test to see if button press toggles are working.
        if controller_toggles[enums.ControllerButtonNames.B]:
            stop = True
        else:
            stop = False

        # Publish the PWM values to the MQTT broker.
        self._rov_connection.publish_thruster_pwm(pwm_values)
        self._rov_connection.publish_commands({
            "stop": stop,
        })

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
