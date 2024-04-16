
Simple guide to configs 


from typing import NamedTuple
import commands2
import rev
from config import ShooterConfig
from config import PIDConfig
import hardware
import math
import logging

"""
this is an example of a motor config class. 
configs inherit from named tuples (this is a good description of named tuples: https://stackoverflow.com/questions/2970608/what-are-named-tuples-in-python)
the advantage of using configs is that it increases modularity.
configs keep things modular by adding standardization for function and class args. 
they define all the information needed to interact with something
ie: 2 classes do separate things, but since they both talk to motors they would both take a motor config as an arg. 
"""


class MotorConfig(NamedTuple):
    """Information to configure a motor"""
    id: int  # Motor ID on the RoboRIO
    inverted: bool  # Invert the motor
    current_limit: int | None  = None  # Current limit in amps
    open_ramp_rate: float | None = None  # Time in seconds to go from 0 to full throttle
    closed_ramp_rate: float | None = None  # Time in seconds to go from 0 to full throttle


########################################################################################################################
"""
below describes how they are used in the rest of the code:
notice that the config is in another config:
configs can and should be used anywhere they can be.
"""
shooter_config = ShooterConfig(left_motor=MotorConfig(id=11, inverted=False),  # this is how configs can be created.
                               right_motor=MotorConfig(id=12, inverted=True),
                               right_flywheel_gear_ratio=1,
                               left_flywheel_gear_ratio=1,
                               right_flywheel_diameter_cm=12,
                               left_flywheel_diameter_cm=12,
                               default_velocity=1,
                               default_fire_time=.5,
                               default_spinup_delay=1)
########################################################################################################################
"""
if we take a look a snippet from the shooter class, we can see how configs are used when making classes:
"""

class Shooter(commands2.Subsystem):
    _left_motor: rev.CANSparkMax
    _right_motor: rev.CANSparkMax
    _left_encoder: rev.SparkRelativeEncoder
    _right_encoder: rev.SparkRelativeEncoder
    _pid: rev.SparkMaxPIDController
    _logger: logging.Logger
    config: ShooterConfig

    def __init__(self, config: ShooterConfig, pid_config: PIDConfig, logger: logging.Logger):
        super().__init__()
        self.config = config
        self._logger = logger.getChild("Shooter")
        self._left_motor = rev.CANSparkMax(config.left_motor.id, rev.CANSparkMax.MotorType.kBrushless)  # notice use of configs 
        self._right_motor = rev.CANSparkMax(config.right_motor.id, rev.CANSparkMax.MotorType.kBrushless)
        hardware.init_motor(self._left_motor, config.left_motor)
        hardware.init_motor(self._right_motor, config.right_motor)

        self._right_motor.follow(self._left_motor, invert=config.right_motor.inverted)
        self._left_encoder = self._left_motor.getEncoder()
        self._right_encoder = self._right_motor.getEncoder()

        self._right_encoder.setPositionConversionFactor(
            (1 / config.right_flywheel_gear_ratio) * ((config.right_flywheel_diameter_cm / 100) * math.pi))
        self._left_encoder.setPositionConversionFactor(
            (1 / config.left_flywheel_gear_ratio) * (config.left_flywheel_diameter_cm / 100) * math.pi)

        self._right_encoder.setVelocityConversionFactor(
            (1 / config.right_flywheel_gear_ratio) * ((config.right_flywheel_diameter_cm / 100) * math.pi) / 60.0)
        self._left_encoder.setVelocityConversionFactor(
            (1 / config.left_flywheel_gear_ratio) * ((config.left_flywheel_diameter_cm / 100) * math.pi) / 60.0)

        self._pid = self._left_motor.getPIDController() 
        hardware.init_pid(self._pid, pid_config, feedback_device=self._left_encoder)

    @property
    def pid_config(self) -> PIDConfig:
        return PIDConfig(p=self._pid.getP(), i=self._pid.getI(), d=self._pid.getD())
        
