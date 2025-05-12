"""Module providing a basic wrapper for ROV thrusters and PWM calculations.
Input is given through lateral_thruster_calc_circular and returned as a FrameThrusters object."""

import math
from typing import Sequence

import numpy as np

from config.thruster import ThrusterConfig
# noinspection PyUnresolvedReferences
from enums import ThrusterPositions, Directions
from utilities.vector import Vector3

# Imma be honest, this feels needlessly precise. Why do we need it down to the 10 Quadrillionth place?
INV_SQRT2 = 0.7071067811865476


class ThrusterPWM:
    """Basic wrapper for a servo-based PWM thruster."""

    _thrust: float  # Requested power output, assuming thruster is oriented as the frame expects
    _config: ThrusterConfig
    _pwm: int  # Cached pwm output for current requested power, configuration may reverse polarity if required
    _power: float

    @property
    def config(self) -> ThrusterConfig:
        return self._config

    @property
    def requested_power(self):
        """The requested power output of the motor"""
        return self._power

    @requested_power.setter
    def requested_power(self, value):
        self._power = value
        self._calculate_pwm()

    @property
    def pwm_output(self) -> int:
        """PWM output corresponding to current power setting"""
        return self._pwm

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
        self._calculate_pwm()

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
        # if self._config.reverse_polarity:
        #     force.x = -force.x
        #     force.y = -force.y
        #     force.z = -force.z

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
        # if self._config.reverse_polarity:
        #     torque.x = -torque.x
        #     torque.y = -torque.y
        #     torque.z = -torque.z

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
        actual_power = self.requested_power * self.thrust
        if self.config.reversed_thrust:
            actual_power = -actual_power

        return int(self.min_pwm_output + 0.5 * (self.max_pwm_output - self.min_pwm_output) * (actual_power + 1))

    def __repr__(self) -> str:
        return f"Thruster(power={self.requested_power} pwm={self.pwm_output})"


class FrameThrusters:
    """Wrapper for a ROV frame's thrusters.

       A right handed coordinate system is expected
       The eight motor frame expects the FrontLeft motor to be oriented so positive thrust pushes water to the back of the ROV and to the left of the ROV
       The front and back motors are mirrored.  To go forward the front motors have a value of 1 and the rear motors a value of -1

        """
 
    _current_power: dict[ThrusterPositions, float] = {}

    def __init__(self, thrusters: dict[ThrusterPositions, ThrusterPWM]) -> None:
        """Initialize a new set of thruster values.

        Args:
            thrusters (dict[ThrusterPositions, ThrusterPWM]):
                A dictionary of thrusters.
        """
        self.thrusters = thrusters
        

    @property
    def normalized_output(self):
        return self._current_power

    @property
    def pwm(self) -> dict[ThrusterPositions, int]:
        """Get a PWM value for each thruster at its current power."""
        return {position: thruster.pwm_output for position, thruster in self.thrusters.items()}

    def __repr__(self) -> str:
        return ("FrameThrusters(" +
            f"', '.join([str(thruster) + '=' + str(thruster.pwm_output) for thruster in self.thrusters.values()])" +
        "}")

    def _thruster_calc(self, motions: dict[Directions, float]) -> dict[ThrusterPositions, float]:
        """Calculate thruster values from -1 to 1 for a given set of inputs. Function assumes all 
        thrusters are oriented correctly and not reversed.  Specified orientation changes and different PWM ranges
        should be handled in ThrusterPWM configuration

        Args:
            motions (dict[Directions, float]):
                A dictionary of thruster orientations and their values.

        Returns:
            FrameThrusters: A collection of Thrusters at the correct power levels."""
        key_order = []
        key_forces = []
        # Matrix multiplication using the forces and torques of each thruster to calculate the values needed to achieve
        # the desired direction of motion.

        for key, t in self.thrusters.items():
            key_order.append(key)
            key_forces.append( [t.forces.x, t.forces.y, t.forces.z, t.torques.yaw, t.torques.pitch, t.torques.roll] )

        motor_matrix: np.array = np.array(key_forces)

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

        required_thruster_power = self.scale_output(motor_thrust_array, key_order=key_order, requested_motions=motions)



        #

        # Set the power of each thruster to the calculated value.
#         required_thruster_power = {}
#         for i, position in enumerate(key_order):
#             required_thruster_power[position] = norm_motor_thrust_array[i]
# #            self.thrusters[position].power = norm_motor_thrust_array[i]
        
        return required_thruster_power

    def scale_output(self, input_power: Sequence[float],
                         key_order: list[ThrusterPositions],
                         requested_motions: dict[Directions, float]) -> dict[ThrusterPositions, float]:
        """
        Normalized the input thruster values to ensure the motors deliver output within the requested range.

        :param input_power: Starting power values for each motor
        :param key_order: The order that each thruster position appears in the motor_thrust_matrix
        :param motions: Magnitude of each motion type
        Returns: Thruster power values proportional to the requested input range.
        """
        # Separate lateral and vertical thrusters for independent normalization

        lateral_indices = []
        vertical_indices = []
        lateral_thrusters = []
        vertical_thrusters = []

        for i, position in enumerate(key_order):
            if "_VERTICAL" in str(position):
                vertical_indices.append(i)
                vertical_thrusters.append(input_power[i])
            else:
                lateral_indices.append(i)
                lateral_thrusters.append(input_power[i])

        #Calculate the magnitude of the lateral and vertical thruster inputs

        #To be correct we should take the cube root, but I felt the square root was a smoother response curve.  Needs testing in real life
        horz_magnitude = math.sqrt(requested_motions[Directions.FORWARDS] ** 2 +
                         requested_motions[Directions.RIGHT] ** 2 +
                         requested_motions[Directions.YAW] ** 2)

        vert_magnitude = math.sqrt(requested_motions[Directions.UP] ** 2 +
                                   requested_motions[Directions.ROLL] ** 2 +
                                   requested_motions[Directions.PITCH] ** 2)

        #Ensure values are in the range of 0, 1 - Not needed if cube root is used to calculate magnitude
        horz_magnitude = np.clip(horz_magnitude, 0, 1)
        vert_magnitude = np.clip(vert_magnitude, 0, 1)

        # Normalize lateral thrusters
        norm_motor_thrust_array = input_power.copy()
        lateral_norm_max = max([abs(val) for val in lateral_thrusters]) if lateral_thrusters else 1
        lateral_norm_scalar = horz_magnitude / lateral_norm_max if lateral_norm_max != 0 else 0
        for i in lateral_indices:
            norm_motor_thrust_array[i] = input_power[i] * lateral_norm_scalar

        # Normalize vertical thrusters
        vertical_norm_max = max([abs(val) for val in vertical_thrusters]) if vertical_thrusters else 1
        vertical_norm_scalar = vert_magnitude / vertical_norm_max if vertical_norm_max != 0 else 0
        for i in vertical_indices:
            norm_motor_thrust_array[i] = input_power[i] * vertical_norm_scalar

        thruster_outputs = {}
        for i in lateral_indices:
            key = key_order[i]
            value = norm_motor_thrust_array[i]
            thruster_outputs[key] = value

        for i in vertical_indices:
            key = key_order[i]
            value = norm_motor_thrust_array[i]
            thruster_outputs[key] = value

        return thruster_outputs


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

    def update_thruster_output(self, motions: dict[Directions, float]) -> dict[ThrusterPositions, int]:
        """Get PWM values for a given set of inputs. USE THIS FUNCTION, NOT THE OTHERS, FROM OUTSIDE THE THRUSTER_PWM
        FILE.

        Args:
            motions (dict[Directions, float]):
                A dictionary of thruster orientations and their values.

        Returns:
            list[int]: PWM values for each thruster.
        """
        self._current_power = self._thruster_calc(motions)

        for position in list(ThrusterPositions):
            self.thrusters[position].thrust = self._current_power[position]

