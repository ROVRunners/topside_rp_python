import unittest
import math
from utilities.vector import Vector3
from wpimath.geometry import Quaternion
import pytest
import numpy as np

class quat_test(unittest.TestCase):

    def setQuat(self, attq):
        self._attitude_quat = Quaternion(
        w=attq[0], x=attq[1], y=attq[2], z=attq[3])

    def quat_to_vector3(self, attitude_quat):
        attitude = []
        quat = attitude_quat.normalize().toRotationVector()  #remove .normalize later
        for q in quat:
            attitude.append(q)
        return Vector3(yaw=attitude[0], pitch=attitude[1], roll=attitude[2])

    def test_quat_to_vector3(self):
        attq = [0.9999999999999999, 0.0, 0.0, 0.0]
        self.setQuat(attq)
        expected = Vector3(yaw=0, pitch=0, roll=0)
        actual = self.quat_to_vector3(self._attitude_quat)
        self.assertEqual(expected, actual)

@pytest.mark.parametrize("quat, expected_euler", [
    (Quaternion(1, 0, 0, 0), (0.0, 0.0, 0.0)),  # Example test case
    (Quaternion(0, 1, 0, 0), (np.pi, 0.0, 0.0)),  # Adjust expected values accordingly
    (Quaternion(0, 0, 1, 0), (0.0, np.pi, 0.0)),
    (Quaternion(0, 0, 0, 1), (0.0, 0.0, np.pi)),
    (Quaternion(0, 0, 0, .5), (0.0, 0.0, np.pi)),
])
def test_quaternion_to_euler(quat, expected_euler):
    quat = quat.normalize()
    euler_angles = quat.toRotationVector()
    assert np.allclose(euler_angles, expected_euler, atol=1e-5)

