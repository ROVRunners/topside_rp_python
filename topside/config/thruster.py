from typing import NamedTuple
from config.range import IntRange

class ThrusterPWMConfig(NamedTuple):
    pwm_pulse_range: IntRange
    reverse_polarity: bool = False
