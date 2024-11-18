from typing import NamedTuple

# from config.typed_range import IntRange
# from config.enums import ThrusterOrientations
import config.typed_range as typed_range
import config.enums as enums


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
    pwm_pulse_range: typed_range.IntRange
    thruster_impulses: dict = {
        enums.Directions.FORWARDS: 0,
        enums.Directions.RIGHT: 0,
        enums.Directions.UP: 0,
        enums.Directions.YAW: 0,
        enums.Directions.PITCH: 0,
        enums.Directions.ROLL: 0,
    }
    reverse_polarity: bool = False




