from typing import NamedTuple

import config.typed_range as typed_range
from utilities.vector import Vector3


class ThrusterConfig(NamedTuple):
    """Configuration for a PWM thruster.

    Attributes:
        pwm_pulse_range (IntRange):
            The range of PWM pulses that the thruster can accept.
        thruster_position (Vector3):
            The position of the thruster on the ROV. This is the position of the thruster relative to the center of
            the ROV.
                X is measured from the center of the ROV to the right.
                Y is measured from the center of the ROV to the front.
                Z is measured from the center of the ROV to the top.
        thruster_orientation (Vector3):
            The orientation of the thruster on the ROV. This is the direction that the thruster will push towards.
                Yaw is measured counterclockwise from the front around the vertical (z) axis and is represented by
            rotating to the left.
                Pitch is measured counterclockwise from the horizontal (x) axis and is represented by rotating
            the front up.
                Roll is measured counterclockwise from the right side around the front (y) axis and is represented by
            rotating the right side up. Note that this is not used for thrusters as rolling a thruster about the axis in
            which it pushes changes nothing.
        thrust (float):
            The thrust of the thruster. This is a scalar value that determines the force that the thruster will
            generate. The value is unitless and is only used to compare the relative thrust of different thrusters.
        reverse_polarity (bool):
            Whether the thruster has reverse polarity.
    """
    pwm_pulse_range: typed_range.IntRange
    thruster_position: Vector3 = Vector3(0, 0, 0)
    thruster_orientation: Vector3 = Vector3(0, 0, 0)
    thrust: float = 1.0
    reverse_polarity: bool = False
