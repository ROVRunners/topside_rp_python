from typing import NamedTuple
from config.range import IntRange


class ThrusterPWMConfig(NamedTuple):
    pwm_pulse_range: IntRange
    thruster_impulses: dict = {
                                "forwards": 0,
                                "right": 0,
                                "up": 0,
                                "pitch": 0,
                                "roll": 0,
                                "yaw": 0,
                                }
    reverse_polarity: bool = False




