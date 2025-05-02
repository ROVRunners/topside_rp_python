"""Module providing a basic wrapper for ROV thrusters and PWM calculations.
Input is given through lateral_thruster_calc_circular and returned as a FrameThrusters object."""

import math

import numpy as np

from config.thruster import ThrusterConfig
# noinspection PyUnresolvedReferences
from enums import ThrusterPositions, Directions
from utilities.vector import Vector3

# Imma be honest, this feels needlessly precise. Why do we need it down to the 10 Quadrillionth place?
INV_SQRT2 = 0.7071067811865476


class ThrusterPWM:
    """Basic wrapper for a servo-based PWM thruster."""

    _power: float
    _config: ThrusterConfig
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
        self._power = value
        self._pwm = self._calculate_pwm()

    @property
    def min_pwm_output(self) -> int:
        return self._config.pwm_pulse_range.min

    @property
    def max_pwm_output(self) -> int:
        return self._config.pwm_pulse_range.max

    @property
    def torques(self) -> Vector3:
        """The torque applied by the thruster in each direction."""
        return self._torques

    @property
    def forces(self) -> Vector3:
        """The thrust applied by the thruster in each direction."""
        return self._forces

    @property
    def position(self) -> Vector3:
        """The position of the thruster in the ROV."""
        return self._position

    @property
    def orientation(self) -> Vector3:
        """The orientation of the thruster in the ROV."""
        return self._orientation

    @property
    def thrust(self) -> float:
        """The thrust applied by the thruster."""
        return self._thrust

    @position.setter
    def position(self, value: Vector3):
        """Set the position of the thruster in the ROV."""
        self._position = value
        self.calculate_torques()

    @orientation.setter
    def orientation(self, value: Vector3):
        """Set the orientation of the thruster in the ROV."""
        self._orientation = value
        self.calculate_forces()
        self.calculate_torques()

    @thrust.setter
    def thrust(self, value: float):
        """Set the thrust applied by the thruster."""
        self._thrust = value
        self.calculate_forces()
        self.calculate_torques()

    @property
    def reverse_polarity(self) -> bool:
        """Whether the thruster is reversed or not."""
        return self._reverse_polarity

    def __init__(self, thruster_config: ThrusterConfig, power: float = 0.0):
        """Initialize a new thruster

        Args:
            thruster_config (ThrusterConfig):
                Configuration for the thruster.
            power (float):
                Motor power.
                Defaults to 0.0.
        """
        self._config = thruster_config
        self._name = thruster_config.name
        self._pwm = self.min_pwm_output
        self._power = power
        self._position = thruster_config.thruster_position
        self._orientation = thruster_config.thruster_orientation
        self._thrust = thruster_config.thrust
        self._reverse_polarity = thruster_config.reverse_polarity

        self._forces: Vector3 = Vector3()
        self._torques: Vector3 = Vector3()

        # Calculate the forces and torques applied by the thruster in each direction.
        self.calculate_forces()
        self.calculate_torques()

        print(f"{self._name} torques: {self._torques}")

    def calculate_forces(self) -> None:
        """Calculate or recalculate the lateral forces applied by the thruster in each direction."""
        force: Vector3 = Vector3(
            x=self._thrust * math.sin(math.radians(self._orientation.yaw)) * math.cos(math.radians(self._orientation.pitch)),
            y=self._thrust * math.cos(math.radians(self._orientation.yaw)) * math.cos(math.radians(self._orientation.pitch)),
            z=self._thrust * math.sin(math.radians(self._orientation.pitch)),
        )

        # Get rid of small values to avoid floating point errors because they're annoying.
        if abs(force.x) < 0.001:
            force.x = 0.0
        if abs(force.y) < 0.001:
            force.y = 0.0
        if abs(force.z) < 0.001:
            force.z = 0.0

        print(f"{self._name} forces: {force}")

        # Apply the reverse polarity if needed.
        if self._config.reverse_polarity:
            force.x = -force.x
            force.y = -force.y
            force.z = -force.z

        self._forces = force

    def calculate_torques(self) -> None:
        """Calculate or recalculate the torques applied by the thruster in each direction."""

        # Calculate the angle of the thruster relative to the line drawn from the center of mass to the thruster to
        # determine the proportion of torque that the thruster will apply in each direction.

        torque_angles = Vector3(
            yaw=(
                self._angle_math(
                    self._orientation.yaw,
                    self._position.x,
                    self._position.y
                )
            ),
            pitch=(
                self._angle_math(
                    self._orientation.pitch + 90,
                    self._position.y,
                    self._position.z
                )
            ),
            roll=(
                self._angle_math(
                    self._orientation.roll,
                    self._position.x,
                    self._position.z
                )
            ),
        )

        # Calculate the torques that the thruster will apply in each direction based on the relative force of the
        # thruster, the distance from the center of mass, and the angle of the thruster.
        torque: Vector3 = Vector3(
            yaw=self._position.magnitude * self._thrust * torque_angles.yaw,
            pitch=self._position.magnitude * self._thrust * torque_angles.pitch,
            roll=self._position.magnitude * self._thrust * torque_angles.roll,
        )

        # Get rid of small values to avoid floating point errors because they're annoying.
        if abs(torque.yaw) < 0.001:
            torque.yaw = 0.0
        if abs(torque.pitch) < 0.001:
            torque.pitch = 0.0
        if abs(torque.roll) < 0.001:
            torque.roll = 0.0

        # Apply the reverse polarity if needed.
        if self._config.reverse_polarity:
            torque.x = -torque.x
            torque.y = -torque.y
            torque.z = -torque.z

        self._torques = torque
    
    @classmethod
    def _angle_math(cls, orient: float, pos_1: float, pos2: float) -> float:
        if pos2 > 0:
            return math.sin(math.radians(180-orient) - math.atan(pos_1/pos2))
        elif pos2 < 0:
            return math.sin(math.radians(360-orient) - math.atan(pos_1/pos2))
        
        else:
            return (pos_1 / abs(pos_1)) * math.sin(math.radians(180-orient) - math.radians(90)) if pos_1 != 0 else 0

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
        return ("FrameThrusters(" +
            f"', '.join([str(thruster) + '=' + str(thruster.pwm_output) for thruster in self.thrusters.values()])" +
        "}")

    def _thruster_calc(self, motions: dict[Directions, float]) -> None:
        """Calculate thruster values for a given set of inputs.

        Args:
            motions (dict[Directions, float]):
                A dictionary of thruster orientations and their values.

        Returns:
            FrameThrusters: A collection of Thrusters at the correct power levels."""

        # Matrix multiplication using the forces and torques of each thruster to calculate the values needed to achieve
        # the desired direction of motion.
        motor_matrix: np.array = np.array([
            [t.forces.x, t.forces.y, t.forces.z, t.torques.yaw, t.torques.pitch, t.torques.roll]
            for t in self.thrusters.values()
        ])

        desired_direction_matrix: np.array = np.array([
            [motions[Directions.FORWARDS]],
            [motions[Directions.RIGHT]],
            [motions[Directions.UP]],
            [motions[Directions.YAW]],
            [motions[Directions.PITCH]],
            [motions[Directions.ROLL]],
        ])

        motor_thrust_matrix: np.array = motor_matrix @ desired_direction_matrix

        # The result of the matrix multiplication is a 8x1 matrix.
        motor_thrust_array: list[float] = list(motor_thrust_matrix.flatten())

        # Normalize the values to be in the range [-1.0, 1.0].
        norm_motor_thrust_array = motor_thrust_array.copy()

        norm_div = max([abs(val) for val in motor_thrust_array])
        if norm_div != 0:
            for i, val in enumerate(norm_motor_thrust_array):
                norm_motor_thrust_array[i] = val / norm_div

        # Scale the values to be proportional to the highest value in the desired directions. Skip if the multiplier is
        # 1.0, as this means that the values are already normalized.
        multiplier = max([abs(val) for val in motions.values()])
        if multiplier != 1:
            for i, val in enumerate(norm_motor_thrust_array):
                norm_motor_thrust_array[i] = val * multiplier

        # Set the power of each thruster to the calculated value.
        for i, position in enumerate(self.thrusters.keys()):
            self.thrusters[position].power = norm_motor_thrust_array[i]

    # TODO: This function should probably be moved into the ROV-specific files
    @classmethod
    def _map_to_circle(cls, x: float, y: float) -> tuple[float, float]:
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
