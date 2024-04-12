import math

from Surface_Python.utilities import Range

tau = math.pi * 2


def wrap_angle(angle: float, min_val: float = 0) -> float:
    """Wrap the angle to the range of 0 to 2pi"""
    clamped = angle % tau

    max_val = min_val + tau
    while clamped >= max_val:  # TODO Do the math and multiply instead of adding
        clamped -= tau
    while clamped < min_val:
        clamped += tau
    return clamped


def wrap_angle_degrees(angle: float, min_val: float = 0) -> float:
    """Wrap the angle to the range of 0 to 2pi"""
    clamped = angle % 360.0
    max_val = min_val + 360.0
    while clamped >= max_val:  # TODO Do the math and multiply instead of adding
        clamped -= 360.0
    while clamped < min_val:
        clamped += 360.0
    return clamped


def shortest_angle_difference(angle1: float, angle2: float) -> float:
    """Returns the shortest angle difference between two angles"""
    diff = (angle2 - angle1 + math.pi) % (math.pi * 2) - math.pi
    return diff


# def optimize_state_improved(desired_state: kinematics.SwerveModuleState,
#                             current_angle: geom.Rotation2d) -> kinematics.SwerveModuleState:
#     """Returns the optimized angle for a swerve module.  This is a modified version of the wpilib implementation that
#        uses the dot product to determine angle reversal and scales the output speed according to the dot product as
#        well."""
#     desired_angle = desired_state.angle
#     desired_vector = np.array([desired_angle.cos(), desired_angle.sin()])
#     current_vector = np.array([current_angle.cos(), current_angle.sin()])
#     result = np.vdot(desired_vector, current_vector)  # type: float # type: ignore
#     if __debug__:
#         assert (-1.00001 <= result <= 1.00001)  # Use an epsilon to account for floating point errors
#
#     desired_speed = desired_state.speed * result
#
#     if np.isclose(result, 0):  # If the dot product is 0, we don't need to change the angle
#         desired_speed = 0
#         desired_state = kinematics.SwerveModuleState(desired_speed, desired_angle)
#     # If the dot product is negative, we need to reverse the desired angle, and scale speed by the dot product
#     elif result < 0:
#         desired_angle = desired_angle + geom.Rotation2d(math.pi)
#         desired_state = kinematics.SwerveModuleState(desired_speed, desired_angle)
#     else:  # No change needed to the desired angle
#         desired_state = kinematics.SwerveModuleState(desired_speed, desired_angle)
#
#     return desired_state


def map_input_to_output_range(value: float, input_range: Range, output_range: Range):
    """Takes an input that lies within a range, and maps it proportionally to the output range.
       For example, given an input range 0.1 to 1, and output range 0 to 10, and an input value of
       0.55, this function will return 5, as it is halfway through the input range, and halfway
       through the output range is 5.
       Useful for mapping input from a controller axis to a desired robot travel speed with a deadband
       """
    input_norm = input_range.normalize(abs(value))
    # input_one_norm = self.inputControllerOneRange.normalize(abs(input))
    if input_norm > 0:
        input_adjusted = output_range.interpolate(input_norm)
        input_adjusted = input_adjusted if value >= 0 else -input_adjusted
    else:
        input_adjusted = 0

    return input_adjusted
