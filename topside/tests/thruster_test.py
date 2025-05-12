import unittest
import math
import numpy as np

import enum
from rovs.spike.enums import Directions
from hardware import thruster_pwm
from rovs.spike import rov_config
from rovs.spike.enums import ThrusterPositions
from utilities.range_util import Range

class thruster_test(unittest.TestCase):


    def calc_pwm(self, power):
        power *= 0.7
        return int(1100 + 0.5 * (1900 - 1100) * (power + 1))

    def setUp(self):
        self._config = rov_config.ROVConfig()
        self._thrusters = {}
        self._pwm_range = Range(-1, 1)

        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)
        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

    def test_forward(self):
        expected = {
         ThrusterPositions.FRONT_RIGHT: 1,
         ThrusterPositions.FRONT_LEFT: 1,
         ThrusterPositions.REAR_RIGHT: -1,
         ThrusterPositions.REAR_LEFT: -1,
         ThrusterPositions.FRONT_RIGHT_VERTICAL: 0,
         ThrusterPositions.FRONT_LEFT_VERTICAL: 0,
         ThrusterPositions.REAR_RIGHT_VERTICAL: 0,
         ThrusterPositions.REAR_LEFT_VERTICAL: 0
        }

        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: 1,
                Directions.RIGHT: 0,
                Directions.UP: 0,
                Directions.YAW: 0,
                Directions.PITCH: 0,
                Directions.ROLL: 0,
            })

        actual = self._frame.normalized_output

        self.compare_motor_states(expected=expected, actual=actual)

    def test_forward_half_speed(self):
        expected = {
            ThrusterPositions.FRONT_RIGHT: .5,
            ThrusterPositions.FRONT_LEFT: .5,
            ThrusterPositions.REAR_RIGHT: -.5,
            ThrusterPositions.REAR_LEFT: -.5,
            ThrusterPositions.FRONT_RIGHT_VERTICAL: 0,
            ThrusterPositions.FRONT_LEFT_VERTICAL: 0,
            ThrusterPositions.REAR_RIGHT_VERTICAL: 0,
            ThrusterPositions.REAR_LEFT_VERTICAL: 0
        }

        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: 0.5,
                Directions.RIGHT: 0,
                Directions.UP: 0,
                Directions.YAW: 0,
                Directions.PITCH: 0,
                Directions.ROLL: 0,
            })

        actual = self._frame.normalized_output

        self.compare_motor_states(expected=expected, actual=actual)

    def test_up(self):
        expected = {
         ThrusterPositions.FRONT_RIGHT: 0,
         ThrusterPositions.FRONT_LEFT: 0,
         ThrusterPositions.REAR_RIGHT: 0,
         ThrusterPositions.REAR_LEFT: 0,
         ThrusterPositions.FRONT_RIGHT_VERTICAL: 1,
         ThrusterPositions.FRONT_LEFT_VERTICAL: 1,
         ThrusterPositions.REAR_RIGHT_VERTICAL: 1,
         ThrusterPositions.REAR_LEFT_VERTICAL: 1
        }

        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: 0,
                Directions.RIGHT: 0,
                Directions.UP: 1,
                Directions.YAW: 0,
                Directions.PITCH: 0,
                Directions.ROLL: 0,
            })

        actual = self._frame.normalized_output

        self.compare_motor_states(expected=expected, actual=actual)

    def test_forward_up(self):
        expected = {
         ThrusterPositions.FRONT_RIGHT: 1,
         ThrusterPositions.FRONT_LEFT: 1,
         ThrusterPositions.REAR_RIGHT: -1,
         ThrusterPositions.REAR_LEFT: -1,
         ThrusterPositions.FRONT_RIGHT_VERTICAL: 1,
         ThrusterPositions.FRONT_LEFT_VERTICAL: 1,
         ThrusterPositions.REAR_RIGHT_VERTICAL: 1,
         ThrusterPositions.REAR_LEFT_VERTICAL: 1
        }

        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: 1,
                Directions.RIGHT: 0,
                Directions.UP: 1,
                Directions.YAW: 0,
                Directions.PITCH: 0,
                Directions.ROLL: 0,
            })

        actual = self._frame.normalized_output

        self.compare_motor_states(expected=expected, actual=actual)

    def test_strafe_right(self):
        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: 0,
                Directions.RIGHT: 1,
                Directions.UP: 0,
                Directions.YAW: 0,
                Directions.PITCH: 0,
                Directions.ROLL: 0,
            })

        actual = self._frame.normalized_output

        expected = {
            ThrusterPositions.FRONT_RIGHT: -1,
            ThrusterPositions.FRONT_LEFT: 1,
            ThrusterPositions.REAR_RIGHT: -1,
            ThrusterPositions.REAR_LEFT: 1,
            ThrusterPositions.FRONT_RIGHT_VERTICAL: 0,
            ThrusterPositions.FRONT_LEFT_VERTICAL: 0,
            ThrusterPositions.REAR_RIGHT_VERTICAL: 0,
            ThrusterPositions.REAR_LEFT_VERTICAL: 0,
        }

        self.compare_motor_states(expected=expected, actual=actual)

    def test_turn_right(self):
        self._frame.update_thruster_output(
            {
                Directions.FORWARDS: 0,
                Directions.RIGHT: 0,
                Directions.UP: 0,
                Directions.YAW: 1,
                Directions.PITCH: 0,
                Directions.ROLL: 0,
            })

        actual = self._frame.normalized_output

        expected = {
            ThrusterPositions.FRONT_RIGHT: -1,
            ThrusterPositions.FRONT_LEFT: 1,
            ThrusterPositions.REAR_RIGHT: 1,
            ThrusterPositions.REAR_LEFT: -1,
            ThrusterPositions.FRONT_RIGHT_VERTICAL: 0,
            ThrusterPositions.FRONT_LEFT_VERTICAL: 0,
            ThrusterPositions.REAR_RIGHT_VERTICAL: 0,
            ThrusterPositions.REAR_LEFT_VERTICAL: 0,
        }

        self.compare_motor_states(expected=expected, actual=actual)

    def compare_motor_states(self, expected: dict[ThrusterPositions, float], actual : dict[ThrusterPositions, float]):
        pass_test = True
        for thruster_name in list(ThrusterPositions):
            e = expected[thruster_name]
            a = actual[thruster_name]
            if not math.isclose(e,a):
                print(f'{thruster_name} has unexpected value {a} expected {e}')
                pass_test = False

        self.assertTrue(pass_test, msg=f'At least one thruster has unexpected value')
