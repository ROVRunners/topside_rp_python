from typing import NamedTuple
from config.range import IntRange

class ThrusterConfig(NamedTuple):
    pwm_pulse_range: IntRange
    reverse_polarity: bool = False
