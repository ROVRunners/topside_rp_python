"""This file contains the configuration for the Spike ROV."""

from config.enums import ControllerAxisNames, ControllerButtonNames, ThrusterPositions, ThrusterOrientations
from topside.config import AxisConfig, ButtonConfig, ThrusterPWMConfig, IntRange, ControllerConfig


class SpikeConfig:
    """Class for the ROV  configuration."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        self.controller_axis_mapping: dict[ControllerAxisNames, int] = {
            ControllerAxisNames.LEFT_X: 0,
            ControllerAxisNames.LEFT_Y: 1,
            ControllerAxisNames.RIGHT_X: 2,
            ControllerAxisNames.RIGHT_Y: 3,
            ControllerAxisNames.LEFT_TRIGGER: 4,
            ControllerAxisNames.RIGHT_TRIGGER: 5,
        }

        # Put specific settings for each axis here
        self.axis_configs: dict[ControllerAxisNames, AxisConfig] = {
            self.controller_axis_mapping[ControllerAxisNames.LEFT_X]: AxisConfig(deadband=0.15),
            self.controller_axis_mapping[ControllerAxisNames.LEFT_Y]: AxisConfig(deadband=0.15),
            self.controller_axis_mapping[ControllerAxisNames.RIGHT_X]: AxisConfig(deadband=0.15),
            self.controller_axis_mapping[ControllerAxisNames.RIGHT_Y]: AxisConfig(deadband=0.15),
            self.controller_axis_mapping[ControllerAxisNames.LEFT_TRIGGER]: AxisConfig(),
            self.controller_axis_mapping[ControllerAxisNames.RIGHT_TRIGGER]: AxisConfig()
        }
        self.button_configs: dict[ControllerButtonNames, ButtonConfig] = {
            ControllerButtonNames.A.value: ButtonConfig(index=0),
            ControllerButtonNames.B.value: ButtonConfig(index=1),
            ControllerButtonNames.X.value: ButtonConfig(index=2),
            ControllerButtonNames.Y.value: ButtonConfig(index=3),
            ControllerButtonNames.START.value: ButtonConfig(index=6),
            ControllerButtonNames.SELECT.value: ButtonConfig(index=7),
            ControllerButtonNames.LEFT_BUMPER.value: ButtonConfig(index=4),
            ControllerButtonNames.RIGHT_BUMPER.value: ButtonConfig(index=5),
        }

        self.controller_config = ControllerConfig(self.button_configs, self.axis_configs)

        # Definitions of the forces applied by the thrusters.
        self.thruster_impulses: dict[ThrusterPositions, dict[ThrusterOrientations, float]] = {
            ThrusterPositions.FRONT_RIGHT: {
                ThrusterOrientations.FORWARDS: .7,
                ThrusterOrientations.RIGHT: -.7,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: 1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.FRONT_LEFT: {
                ThrusterOrientations.FORWARDS: .7,
                ThrusterOrientations.RIGHT: .7,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: -1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.REAR_RIGHT: {
                ThrusterOrientations.FORWARDS: -.7,
                ThrusterOrientations.RIGHT: -.7,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: 1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.REAR_LEFT: {
                ThrusterOrientations.FORWARDS: -.7,
                ThrusterOrientations.RIGHT: .7,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: -1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.FRONT_RIGHT_VERTICAL: {
                ThrusterOrientations.FORWARDS: 0,
                ThrusterOrientations.RIGHT: -0,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: 1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.FRONT_LEFT_VERTICAL: {
                ThrusterOrientations.FORWARDS: 0,
                ThrusterOrientations.RIGHT: 0,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: -1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.REAR_RIGHT_VERTICAL: {
                ThrusterOrientations.FORWARDS: -0,
                ThrusterOrientations.RIGHT: -0,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: 1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
            ThrusterPositions.REAR_LEFT_VERTICAL: {
                ThrusterOrientations.FORWARDS: -0,
                ThrusterOrientations.RIGHT: 0,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: -1,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
        }

        self.thruster_positions = [
            ThrusterPositions.FRONT_RIGHT,
            ThrusterPositions.FRONT_LEFT,
            ThrusterPositions.REAR_RIGHT,
            ThrusterPositions.REAR_LEFT,
            ThrusterPositions.FRONT_RIGHT_VERTICAL,
            ThrusterPositions.FRONT_LEFT_VERTICAL,
            ThrusterPositions.REAR_RIGHT_VERTICAL,
            ThrusterPositions.REAR_LEFT_VERTICAL,
        ]

        self.thruster_configs: dict[ThrusterPositions, ThrusterPWMConfig] = {

            position: ThrusterPWMConfig(
                pwm_pulse_range=IntRange(min=1100, max=1900),
                thruster_impulses=self.thruster_impulses[position]
            ) for position in self.thruster_positions
        }
