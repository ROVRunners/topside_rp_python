from config.imu import IMUConfig
from i2c import I2C

class IMU:

    def __init__(self, imuconfig: IMUConfig):
        self.imuconfig = imuconfig

        self._accel_x = 0.0
        self._accel_y = 0.0
        self._accel_z = 0.0

        self._yaw = 0.0
        self._roll = 0.0
        self._pitch = 0.0

    def update(self, imu: I2C):
        if not imu.received_vals:
            return
        
        if self.imuconfig.gyro_name in imu.received_vals:
            gyro = imu.received_vals[self.imuconfig.gyro_name]

            self._yaw = gyro['0'] | (gyro['1'] >> 8)
            self._roll = gyro['2'] | (gyro['3'] >> 8)
            self._pitch = gyro['4'] | (gyro['5'] >> 8)

            print("Gyro:", self._yaw, self._pitch, self._roll, end=" | ")

        if self.imuconfig.accel_name in imu.received_vals:
            accel = imu.received_vals[self.imuconfig.accel_name]

            self._accel_x = accel['0'] | (accel['1'] >> 8)
            self._accel_y = accel['2'] | (accel['3'] >> 8)
            self._accel_z = accel['4'] | (accel['5'] >> 8)

            print("Accel:", self._accel_x, self._accel_y, self._accel_z)


    def initialize_imu(self, imu: I2C):
        imu.sending_vals[self.imuconfig.gyro_init_register] = self.imuconfig.gyro_init_value
        imu.sending_vals[self.imuconfig.accel_init_register] = self.imuconfig.accel_init_value


    @property
    def accel_x(self):
        return self._accel_x

    @property
    def accel_y(self):
        return self._accel_y

    @property
    def accel_z(self):
        return self._accel_z

    @property
    def yaw(self):
        return self._yaw

    @property
    def roll(self):
        return self._roll

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = value


