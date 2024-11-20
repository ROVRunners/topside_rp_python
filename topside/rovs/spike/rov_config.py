"""This file contains the configuration for the Spike ROV."""

# from config.enums import ControllerAxisNames, ControllerButtonNames, ThrusterPositions, ThrusterOrientations
# from topside.config import AxisConfig, ButtonConfig, ThrusterPWMConfig, IntRange, ControllerConfig
import config.typed_range as typed_range
import rovs.spike.enums as enums
import config.controller as controller
import config.thruster as thruster


class ROVConfig:
    """Class for the ROV configuration."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # The ports used to communicate with the ROV. The comms port is for the MQTT broker, while the video port is
        # for the video stream(s).
        self.comms_port = 1883
        self.video_port = 5600
        # TODO: This is where you change the IP. It needs to be the local IP for remote stuff to connect.
        #  We need to make it so it 
        self.host_ip = "172.17.128.243"

        # Put specific settings for each axis/button here
        self.axis_configs: dict[enums.ControllerAxisNames, controller.AxisConfig] = {
            enums.ControllerAxisNames.LEFT_X: controller.AxisConfig(index=0, deadband=0.15),
            enums.ControllerAxisNames.LEFT_Y: controller.AxisConfig(index=1, deadband=0.15),
            enums.ControllerAxisNames.RIGHT_X: controller.AxisConfig(index=2, deadband=0.15),
            enums.ControllerAxisNames.RIGHT_Y: controller.AxisConfig(index=3, deadband=0.15),
            enums.ControllerAxisNames.LEFT_TRIGGER: controller.AxisConfig(index=4),
            enums.ControllerAxisNames.RIGHT_TRIGGER: controller.AxisConfig(index=5),
        }
        self.button_configs: dict[enums.ControllerButtonNames, controller.ButtonConfig] = {
            enums.ControllerButtonNames.A: controller.ButtonConfig(index=0),
            enums.ControllerButtonNames.B: controller.ButtonConfig(index=1),
            enums.ControllerButtonNames.X: controller.ButtonConfig(index=2),
            enums.ControllerButtonNames.Y: controller.ButtonConfig(index=3),
            enums.ControllerButtonNames.START: controller.ButtonConfig(index=6),
            enums.ControllerButtonNames.SELECT: controller.ButtonConfig(index=7),
            enums.ControllerButtonNames.LEFT_BUMPER: controller.ButtonConfig(index=4),
            enums.ControllerButtonNames.RIGHT_BUMPER: controller.ButtonConfig(index=5),
        }

        self.controller_config = controller.ControllerConfig(self.button_configs, self.axis_configs)

        # Definitions of the forces applied by the thrusters.
        self.thruster_impulses: dict[enums.ThrusterPositions, dict[enums.Directions, float]] = {
            enums.ThrusterPositions.FRONT_RIGHT: {
                enums.Directions.FORWARDS: 1,
                enums.Directions.RIGHT: -1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: 1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.FRONT_LEFT: {
                enums.Directions.FORWARDS: 1,
                enums.Directions.RIGHT: 1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: -1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.REAR_RIGHT: {
                enums.Directions.FORWARDS: -1,
                enums.Directions.RIGHT: -1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: 1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.REAR_LEFT: {
                enums.Directions.FORWARDS: -1,
                enums.Directions.RIGHT: 1,
                enums.Directions.UP: 0,
                enums.Directions.YAW: -1,
                enums.Directions.PITCH: 0,
                enums.Directions.ROLL: 0,
            },
            enums.ThrusterPositions.FRONT_RIGHT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: 1,
                enums.Directions.ROLL: -1,
            },
            enums.ThrusterPositions.FRONT_LEFT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: 1,
                enums.Directions.ROLL: 1,
            },
            enums.ThrusterPositions.REAR_RIGHT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: -1,
                enums.Directions.ROLL: -1,
            },
            enums.ThrusterPositions.REAR_LEFT_VERTICAL: {
                enums.Directions.FORWARDS: 0,
                enums.Directions.RIGHT: 0,
                enums.Directions.UP: 1,
                enums.Directions.YAW: 0,
                enums.Directions.PITCH: -1,
                enums.Directions.ROLL: 1,
            },
        }

        self.thruster_configs: dict[enums.ThrusterPositions, thruster.ThrusterPWMConfig] = {

            position: thruster.ThrusterPWMConfig(
                pwm_pulse_range=typed_range.IntRange(min=1100, max=1900),
                thruster_impulses=self.thruster_impulses[position]
            ) for position in self.thruster_impulses.keys()
        }
