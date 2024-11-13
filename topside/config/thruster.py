from typing import NamedTuple
from config.range import IntRange
from config.enums import ThrusterOrientations


class ThrusterPWMConfig(NamedTuple):
    """Configuration for a PWM thruster.

    Attributes:
        pwm_pulse_range (IntRange):
            The range of PWM pulses that the thruster can accept.
        thruster_impulses (dict[str, float]):
            The effects of the thruster in each axis.
        reverse_polarity (bool):
            Whether the thruster has reverse polarity.
    """
    pwm_pulse_range: IntRange
    thruster_impulses: dict = {
        ThrusterOrientations.FORWARDS: 0,
        ThrusterOrientations.RIGHT: 0,
        ThrusterOrientations.UP: 0,
        ThrusterOrientations.YAW: 0,
        ThrusterOrientations.PITCH: 0,
        ThrusterOrientations.ROLL: 0,
    }
    reverse_polarity: bool = False




