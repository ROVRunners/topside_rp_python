from typing import NamedTuple

class IMUConfig(NamedTuple):
    gyro_init_register: int
    accel_init_register: int
    gyro_init_value: int
    accel_init_value: int
    gyro_name: str
    accel_name: str

