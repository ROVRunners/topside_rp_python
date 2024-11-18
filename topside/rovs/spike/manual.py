import hardware.thruster_pwm as thruster_pwm
import mqtt_handler
import rovs.spike.enums as enums
import controller_input


class Manual:
    """The manual control class for the ROV."""

    def __init__(self, frame: thruster_pwm.FrameThrusters, rov_connection: mqtt_handler.ROVConnection) -> None:
        """Initialize the Manual object.

        Args:
            frame (thruster_pwm.FrameThrusters):
                The objects of the thrusters mounted to the frame.
            rov_connection (mqtt_handler.ROVConnection):
                The connection to the ROV.
        """

        self._frame = frame
        self._rov_connection = rov_connection

        self._last_pwm_values = {}

        # self.sensor_data = {}
        # self.controller_data = {}
        # self.terminal_data = {}
        # self.pwm_values = []

        # Add whatever you need initialized here.

    @property
    def inputs(self):
        return self.inputs

    @inputs.setter
    def inputs(self, value):
        self.inputs = value

    def update(self, inputs: dict[str, dict[enums.ControllerButtonNames | enums.ControllerAxisNames, any]]):
        """Update thrust values based on the inputs.

        Args:
            inputs (dict[str, dict[enums.ControllerButtonNames | enums.ControllerAxisNames, any]]):
                The inputs from the controller, sensors, and otherwise.
        """
        controller = inputs["controller"]

        # Convert the triggers to a single value.
        right_trigger = controller[enums.ControllerAxisNames.RIGHT_TRIGGER]
        left_trigger = controller[enums.ControllerAxisNames.LEFT_TRIGGER]
        vertical = controller_input.combine_triggers(left_trigger, right_trigger)

        # TODO: Add references any other input processing software like a PID here. Also, a PID should probably be
        #  implemented in a separate class due to it being generally applicable to all ROVs.

        # Get the PWM values for the thrusters.
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

        # Publish the PWM values to the MQTT broker.
        self._rov_connection.publish_thruster_pwm(pwm_values)

        # msgs = []
        # for p, v in pwm_values.items():
        #     msgs.append({'topic': f'thruster_pwm/{p}', "payload": v})
        #
        # publish.multiple(msgs, hostname='localhost', port=1883)
        # publish.single("thruster_pwm", repr(msg), hostname="localhost")

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
