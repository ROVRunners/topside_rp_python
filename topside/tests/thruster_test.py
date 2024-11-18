import unittest

from rovs.spike.enums import ThrusterOrientations
from hardware import thruster_pwm
from rovs.spike import rov_config
from utilities.range import Range

class thruster_test(unittest.TestCase):


    def calc_pwm(self, power):
        power *= 0.7
        return int(1100 + 0.5 * (1900 - 1100) * (power + 1))
    def test_thruster_output(self):
        self._config = rov_config.ROVConfig()
        self._thrusters = {}
        self._pwm_range = Range(1100, 1900)
        # Configure thrusters.
        for position, thruster_config in self._config.thruster_configs.items():
            self._thrusters[position] = thruster_pwm.ThrusterPWM(thruster_config)
        self._frame = thruster_pwm.FrameThrusters(self._thrusters)

        self.assertEqual({
         'FRONT_RIGHT': self.calc_pwm(1),
         'FRONT_LEFT': self.calc_pwm(1),
         'REAR_RIGHT': self.calc_pwm(-1),
         'REAR_LEFT': self.calc_pwm(-1),
         'FRONT_RIGHT_VERTICAL': self.calc_pwm(1),
         'FRONT_LEFT_VERTICAL': self.calc_pwm(1),
         'REAR_RIGHT_VERTICAL': self.calc_pwm(1),
         'REAR_LEFT_VERTICAL': self.calc_pwm(1)
        },
            self._frame.get_pwm_values(
            {
                ThrusterOrientations.FORWARDS: 1,
                ThrusterOrientations.RIGHT: 0,
                ThrusterOrientations.UP: 1,
                ThrusterOrientations.YAW: 0,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
        ))


        self.assertEqual(self._frame.get_pwm_values(
            {
                ThrusterOrientations.FORWARDS: 0,
                ThrusterOrientations.RIGHT: 1,
                ThrusterOrientations.UP: 0,
                ThrusterOrientations.YAW: 0,
                ThrusterOrientations.PITCH: 0,
                ThrusterOrientations.ROLL: 0,
            },
        ),{
         'FRONT_RIGHT': self.calc_pwm(-1),
         'FRONT_LEFT': self.calc_pwm(1),
         'REAR_RIGHT': self.calc_pwm(-1),
         'REAR_LEFT': self.calc_pwm(1),
         'FRONT_RIGHT_VERTICAL': self.calc_pwm(0),
         'FRONT_LEFT_VERTICAL': self.calc_pwm(0),
         'REAR_RIGHT_VERTICAL': self.calc_pwm(0),
         'REAR_LEFT_VERTICAL': self.calc_pwm(0),
        })
