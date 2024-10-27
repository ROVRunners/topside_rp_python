"""Module providing a basic wrapper for ROV thrusters and PWM calculations.
Input is given through lateral_thruster_calc_circular and returned as a FrameThrusters object."""
import math
from config import ThrusterConfig

INV_SQRT2 = 0.7071067811865476


class Thruster:
    """Basic wrapper for a servo-based thruster."""

    _power: float
    _config: ThrusterConfig
    _pwm: int # Cached pwm output for current requested power

    @property
    def power(self) -> float:
        return self._power

    @property
    def pwm_output(self) -> int:
        """PWM output corresponding to current power setting"""
        return self._pwm

    @power.setter
    def power(self, value: float):
        if self._power != value:
            self._power = value
            self._pwm = self._calculate_pwm()

    @property
    def min_pwm_output(self) -> int:
        return self._config.pwm_pulse_range.min

    @property
    def max_pwm_output(self) -> int:
        return self._config.pwm_pulse_range.max

    def __init__(self,
                 thruster_config: ThrusterConfig,
                 power: float = 0.0
                 ):
        """Initialize a new thruster

        :param power:
                Motor power.
                Defaults to 0.0.
        :param reverse_polarity:
                Whether to reverse the output sign
                Defaults to False
        """
        self._config = thruster_config
        self._pwm = self.min_pwm_output
        self._power = power

    def _calculate_pwm(self) -> int:
        """Calculate a PWM value for the thruster at its current power."""
        power = -self.power if self._config.reverse_polarity else self.power
        return int(self.min_pwm_output + 0.5 * (self.max_pwm_output - self.min_pwm_output) * (power + 1))

    def __repr__(self) -> str:
        return f"Thruster(power={self.power} pwm={self.pwm_output})"


class FrameThrusters:
    """Wrapper for a ROV frame's thrusters."""

    def __init__(self, fr: Thruster, fl: Thruster, rr: Thruster, rl: Thruster):
        """Initialize a new set of thruster values.

        Args:
            fr (Thruster):
                Front right thruster.
            fl (Thruster):
                Front left thruster.
            rr (Thruster):
                Rear right thruster.
            rl (Thruster):
                Rear left thruster.
        """
        self.fr = fr
        self.fl = fl
        self.rr = rr
        self.rl = rl

    def get_pwm(self) -> tuple[int, int, int, int]:
        """Get a PWM value for each thruster at its current power."""
        return (
            self.fr.pwm_output,
            self.fl.pwm_output,
            self.rr.pwm_output,
            self.rl.pwm_output
        )

    def __repr__(self) -> str:
        return f"FrameThrusters(ur={self.fr}, ul={self.fl}, lr={self.rr}, ll={self.rl})"


def _lateral_thruster_calc(x: float, y: float, r: float) -> FrameThrusters:
    """Calculate lateral thruster values for a given set of inputs.

    Args:
        x (float):
            Sideways movement speed (between -1.0 and 1.0).
        y (float):
            Forward movement speed (between -1.0 and 1.0).
        r (float):
            Rotation speed (between -1.0 and 1.0).

    Returns:
        FrameThrusters: A collection of Thrusters at the correct power levels."""

    # Assume that positive values are all going forward.
    # We can reason what should happen if we only have a single non-zero input:

    # [x, y, r] -> [ur, ul, lr, ll]
    # [1, 0, 0] -> [-1, +1, +1, -1]
    # [0, 1, 0] -> [+1, +1, +1, +1]
    # [0, 0, 1] -> [+1, +1, -1, -1]

    # We can calculate thruster values as a linear combination of the input values
    # by repeating this pattern with each output scaled by the actual value of each input.

    x_contrib = [-x,  x,  x, -x]
    y_contrib = [y,  y,  y,  y]
    r_contrib = [r,  r, -r, -r]

    # However, we want thruster values to be in the range [-1.0, 1.0], so we need to
    # normalize based on the maximum possible value this can have: 3
    ur = (x_contrib[0] + y_contrib[0] + r_contrib[0]) / 3.0
    ul = (x_contrib[1] + y_contrib[1] + r_contrib[1]) / 3.0
    lr = (x_contrib[2] + y_contrib[2] + r_contrib[2]) / 3.0
    ll = (x_contrib[3] + y_contrib[3] + r_contrib[3]) / 3.0

    return FrameThrusters(Thruster(ur), Thruster(ul), Thruster(lr), Thruster(ll))


def _map_to_circle(x: float, y: float) -> tuple[float, float]:
    """Map rectangular controller inputs to a circle."""

    return x*math.sqrt(1 - y**2/2.0), y*math.sqrt(1 - x**2/2.0)


def _lateral_thruster_calc_circular(x: float, y: float, r: float):
    """Calculate lateral thruster values for a given set of inputs after mapping them to a circle.

    Args:
        x (float):
            Sideways movement speed (between -1.0 and 1.0).
        y (float):
            Forward movement speed (between -1.0 and 1.0).
        r (float):
            Rotation speed (between -1.0 and 1.0).

    Returns:
        FrameThrusters: A collection of Thrusters at the correct power levels."""

    # some bullshit
    x, y = _map_to_circle(x, y)
    r *= INV_SQRT2
    thrusters = _lateral_thruster_calc(x, y, r)
    thrusters.fr.power /= INV_SQRT2
    thrusters.fl.power /= INV_SQRT2
    thrusters.rr.power /= INV_SQRT2
    thrusters.rl.power /= INV_SQRT2

    return thrusters


def _vertical_pwm_calc(z: float, pitch: float, roll: float) -> tuple[int, int]:
    """Calculate vertical thruster values for a given set of inputs.

    Args:
        z (float):
            Vertical movement speed (between -1.0 and 1.0).
        pitch (float):
            Pitch speed (between -1.0 and 1.0).
        roll (float):
            Does nothing here.

    Returns:
        tuple[int, int]: A tuple of PWM values for the vertical thrusters.
    """
    fv = z + pitch
    rv = z - pitch

    # However, we want thruster values to be in the range [-1.0, 1.0], so we need to normalize based on the maximum
    # possible value this can have: 1
    normalization_divisor = max(abs(fv), abs(rv), 1)

    fv /= normalization_divisor
    rv /= normalization_divisor

    # Finally, we need to convert these values to PWM values.
    fv = int(1500 + 400 * fv)
    rv = int(1500 + 400 * rv)

    return fv, rv


def get_pwm_values(x: float = 0, y: float = 0, z: float = 0, yaw: float = 0,
                   pitch: float = 0, roll: float = 0) -> list[int]:
    """Get PWM values for a given set of inputs. USE THIS FUNCTION.

    Args:
        x (float):
            Sideways movement speed (between -1.0 and 1.0).
            Defaults to 0.
        y (float):
            Forward movement speed (between -1.0 and 1.0).
            Defaults to 0.
        z (float):
            Vertical movement speed (between -1.0 and 1.0).
            Defaults to 0.
        yaw (float):
            Rotation speed (between -1.0 and 1.0).
            Defaults to 0.
        pitch (float):
            Pitch speed (between -1.0 and 1.0).
            Defaults to 0.
        roll (float):
            Does nothing here.
            Defaults to 0.

    Returns:
        list[int]: PWM values for each thruster.
    """
    thrusters = _lateral_thruster_calc_circular(x, y, yaw)
    vert_pwm = _vertical_pwm_calc(z, pitch, roll)

    return list(vert_pwm) + list(thrusters.get_pwm())
