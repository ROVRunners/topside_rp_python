from typing import Callable

import hardware.thruster_pwm as thruster_pwm
import mqtt_handler
import rovs.spike.enums as enums
import controller_input


class Manual:
    """The manual control class for the ROV."""

    def __init__(self, frame: thruster_pwm.FrameThrusters, output_map: dict[str, Callable]) -> None:
        """Initialize the Manual object.

        Args:
            frame (thruster_pwm.FrameThrusters):
                The objects of the thrusters mounted to the frame.
            output_map (dict[str, Callable]):
                The output map for the Manual class to access MQTT and other functions.
        """

        self._frame = frame
        self._output_map = output_map

        # Set up the callables for the MQTT handler.
        self._send_commands: mqtt_handler.ROVConnection.publish_commands = output_map["rov_command"]
        self._set_thrusters: mqtt_handler.ROVConnection.publish_thruster_pwm = output_map["rov_thrusters"]

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

    def update(self, inputs: dict[str, dict[enums.ControllerButtonNames | enums.ControllerAxisNames | str, any]]):
        """Update thrust values based on the inputs.

        Args:
            inputs (dict[str, dict[enums.ControllerButtonNames | enums.ControllerAxisNames | str, any]]):
                The inputs from the controller, sensors, and otherwise.
        """
        controller = inputs["controller"]
        subscriptions = inputs["subscriptions"]

        if "ROV_sensor_data" in subscriptions:
            sensor_data = subscriptions["ROV_sensor_data"]

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

        if controller[enums.ControllerButtonNames.B]:
            stop = True
        else:
            stop = False

        # Publish the PWM values to the MQTT broker.
        self._set_thrusters(pwm_values)
        self._send_commands({
            "stop": stop,
        })

    def shutdown(self):
        """Shutdown the ROV."""
        # TODO: Add any shutdown logic here.
        pass
