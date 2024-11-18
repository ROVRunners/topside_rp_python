"""Module providing a basic wrapper for ROV thrusters and PWM calculations.
Input is given through lateral_thruster_calc_circular and returned as a FrameThrusters object."""

import math

from config.thruster import ThrusterPWMConfig
from config.enums import ThrusterPositions, Directions


# Imma be honest, this feels needlessly precise. Why do we need it down to the 10 Quadrillionth place?
INV_SQRT2 = 0.7071067811865476


class ThrusterPWM:
    """Basic wrapper for a servo-based PWM thruster."""

    _power: float
    _config: ThrusterPWMConfig
    _pwm: int  # Cached pwm output for current requested power

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

    @property
    def thruster_impulses(self) -> dict[str, float]:
        return self._impulses

    def __init__(self, thruster_config: ThrusterPWMConfig, power: float = 0.0):
        """Initialize a new thruster

        Args:
            thruster_config (ThrusterPWMConfig):
                Configuration for the thruster.
            power (float):
                Motor power.
                Defaults to 0.0.
        """
        self._config = thruster_config
        self._pwm = self.min_pwm_output
        self._power = power
        self._impulses = thruster_config.thruster_impulses

    def _calculate_pwm(self) -> int:
        """Calculate a PWM value for the thruster at its current power."""
        power = -self.power if self._config.reverse_polarity else self.power
        return int(self.min_pwm_output + 0.5 * (self.max_pwm_output - self.min_pwm_output) * (power + 1))

    def __repr__(self) -> str:
        return f"Thruster(power={self.power} pwm={self.pwm_output})"


class FrameThrusters:
    """Wrapper for a ROV frame's thrusters."""

    def __init__(self, thrusters: dict[ThrusterPositions, ThrusterPWM]) -> None:
        """Initialize a new set of thruster values.

        Args:
            thrusters (dict[ThrusterPositions, ThrusterPWM]):
                A dictionary of thrusters.
        """
        self.thrusters = thrusters

    def get_pwm(self) -> dict[ThrusterPositions, int]:
        """Get a PWM value for each thruster at its current power."""
        return {position: thruster.pwm_output for position, thruster in self.thrusters.items()}

    def __repr__(self) -> str:
        return f"FrameThrusters({', '.join([str(thruster) + '=' + str(thruster.pwm_output) for thruster in self.thrusters.values()])})"

    def _thruster_calc(self, motions: dict[Directions, float]) -> None:
        """Calculate thruster values for a given set of inputs.

        Args:
            motions (dict[Directions, float]):
                A dictionary of thruster orientations and their values.

        Returns:
            FrameThrusters: A collection of Thrusters at the correct power levels."""

        # Assume that positive values are all going forward.
        # We can reason what should happen if we only have a single non-zero input:

        # [x, y, r] -> [fr, fl, rr, rl]
        # [1, 0, 0] -> [-1, +1, +1, -1]
        # [0, 1, 0] -> [+1, +1, +1, +1]
        # [0, 0, 1] -> [+1, +1, -1, -1]

        # We can calculate thruster values as a linear combination of the input values
        # by repeating this pattern with each output scaled by the actual value of each input.

        # x_contrib = [-x,  x,  x, -x]
        # y_contrib = [y,  y,  y,  y]
        # r_contrib = [r,  r, -r, -r]

        # The following is a more general version of the above code. It iterates over all thruster orientations and
        # sums the contributions of each thruster to that orientation.
        orientations = [
            Directions.FORWARDS,
            Directions.RIGHT,
            Directions.UP,
            Directions.PITCH,
            Directions.ROLL,
            Directions.YAW,
        ]

        contributions = {
            orient: [
                self.thrusters[position].thruster_impulses[orient] * motions[orient] for position in self.thrusters.keys()
            ] for orient in orientations
        }

        # Next, we sum the contributions of each thruster to each orientation to get the ratio of power that should be
        # applied to each thruster.
        vals = {
            thruster: sum(contributions[orient][i] for orient in orientations) for i, thruster in enumerate(self.thrusters.keys())
        }

        # However, we want thruster values to be in the range [-1.0, 1.0], so we need to normalize based on the maximum
        # value in the dictionary.
        normalization_divisor = max(abs(val) for val in vals.values())

        # We only need to normalize if the maximum value is greater than 1.
        if normalization_divisor > 1:
            for thruster in self.thrusters.keys():
                vals[thruster] /= normalization_divisor

        # Finally, we set the power of each thruster to the calculated value.
        for position in self.thrusters.keys():
            self.thrusters[position].power = vals[position]

    # TODO: This function should probably be moved into the ROV-specific files
    def _map_to_circle(self, x: float, y: float) -> tuple[float, float]:
        """Map rectangular controller inputs to a circle.

        Args:
            x (float):
                The x-axis of a controller joystick.
            y (float):
                The y-axis of a controller joystick.

        Returns:
            tuple[float, float]: The mapped values.
        """
        return x*math.sqrt(1 - y**2/2.0), y*math.sqrt(1 - x**2/2.0)

    def _thruster_calc_circular(self, motions: dict[Directions, float]) -> None:
        """Calculate thruster values for a given set of desired motions after mapping the lateral controls to a circle.

        Args:
            motions (dict[Directions, float]):
                A dictionary of thruster orientations and their values.

        Returns:
            FrameThrusters: A collection of Thrusters at the correct power levels."""

        # TODO: Figure out what this does and why it's here. Commented it out for now.
        # some bullshit
        # # Map the x and y values to a circle.
        # motions[ThrusterOrientations.FORWARDS], motions[ThrusterOrientations.RIGHT] = (
        #     self._map_to_circle(motions[ThrusterOrientations.FORWARDS], motions[ThrusterOrientations.RIGHT]))
        # # Multiply the yaw value by the inverse square root of 2 for some reason (ask Jackson).
        # motions[ThrusterOrientations.YAW] *= INV_SQRT2
        self._thruster_calc(motions)
        # self.fr.power /= INV_SQRT2
        # self.fl.power /= INV_SQRT2
        # self.rr.power /= INV_SQRT2
        # self.rl.power /= INV_SQRT2

    def get_pwm_values(self, motions: dict[Directions, float]) -> dict[ThrusterPositions, int]:
        """Get PWM values for a given set of inputs. USE THIS FUNCTION, NOT THE OTHERS, FROM OUTSIDE THE THRUSTER_PWM
        FILE.

        Args:
            motions (dict[Directions, float]):
                A dictionary of thruster orientations and their values.

        Returns:
            list[int]: PWM values for each thruster.
        """
        self._thruster_calc_circular(motions)

        return self.get_pwm()
