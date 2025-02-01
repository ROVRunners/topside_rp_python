from config.imu import IMUConfig
from hardware.i2c import I2C
from utilities.ema import EMA
from utilities.riemann_sum import Riemann
from utilities.live_integration import Integration, IntegrationTypes
import time

class IMU:

    def __init__(self, imuconfig: IMUConfig) -> None:
        self.imuconfig = imuconfig

        int_type = IntegrationTypes.TRAPEZOIDAL

        self._yaw_vel_integral = Integration(int_type, 0, time.time(), False)
        self._pitch_vel_integral = Integration(int_type, 0, time.time(), False)
        self._roll_vel_integral = Integration(int_type, 0, time.time(), False)

        self._yaw_integral = Integration(int_type, 0, time.time(), False)
        self._pitch_integral = Integration(int_type, 0, time.time(), False)
        self._roll_integral = Integration(int_type, 0, time.time(), False)

        # self._yaw_vel_riemann = Riemann(self.imuconfig.gyro_conversion_factor)
        # self._pitch_vel_riemann = Riemann(self.imuconfig.gyro_conversion_factor)
        # self._roll_vel_riemann = Riemann(self.imuconfig.gyro_conversion_factor)

        # self._yaw_riemann = Riemann(self.imuconfig.gyro_conversion_factor)
        # self._pitch_riemann = Riemann(self.imuconfig.gyro_conversion_factor)
        # self._roll_riemann = Riemann(self.imuconfig.gyro_conversion_factor)

        self._accel_x = 0.0
        self._accel_y = 0.0
        self._accel_z = 0.0

        self._yaw = 0.0
        self._roll = 0.0
        self._pitch = 0.0

        self._val_considerations = 50
        self._val_smoothing = 5.0

        self._dps = 250.0
        self._g = 2.0

        self._accel_x_ema = EMA(self._val_considerations, self._val_smoothing)
        self._accel_y_ema = EMA(self._val_considerations, self._val_smoothing)
        self._accel_z_ema = EMA(self._val_considerations, self._val_smoothing)

        self._yaw_ema = EMA(self._val_considerations, self._val_smoothing)
        self._roll_ema = EMA(self._val_considerations, self._val_smoothing)
        self._pitch_ema = EMA(self._val_considerations, self._val_smoothing)

        self._yaw_offset = 237
        self._pitch_offset = -122
        self._roll_offset = -235

        self._y_offset = 0
        self._z_offset = 0
        self._x_offset = 0

    def update(self, imu: I2C) -> None:
        """Updates the yaw, pitch, roll, x, y, and z values

        Args:
            imu (I2C): _description_
        """
        if not imu.received_vals:
            return
        
        if self.imuconfig.gyro_name in imu.received_vals:
            gyro = imu.received_vals[self.imuconfig.gyro_name]

            # Combine the bytes.
            raw_yaw = gyro['0'] | (gyro['1'] << 8)
            raw_pitch = gyro['4'] | (gyro['5'] << 8)
            raw_roll = gyro['2'] | (gyro['3'] << 8)

            # Make them signed again (2's compliment).
            signed_yaw = raw_yaw - 32768
            signed_pitch = raw_pitch - 32768
            signed_roll = raw_roll - 32768

            # Normalize the values to the +- dps sensitivity setting we gave earlier.
            norm_yaw = signed_yaw * self._dps / 32768
            norm_pitch = signed_pitch * self._dps / 32768
            norm_roll = signed_roll * self._dps / 32768

            # Subtract the offset values.
            self._yaw_accel = norm_yaw - self._yaw_offset
            self._pitch_accel = norm_pitch - self._pitch_offset
            self._roll_accel = norm_roll - self._roll_offset

            # # Add the values to the Exponential moving average to smooth them out a bit.
            # self._yaw_ema.add(self._yaw_riemann(time.time(), self._yaw_vel_riemann(time.time(), self._yaw)))
            # self._pitch_ema.add(self._pitch_riemann(time.time(), self._pitch_vel_riemann(time.time(), self._pitch)))
            # self._roll_ema.add(self._roll_riemann(time.time(), self._roll_vel_riemann(time.time(), self._roll)))

            # # Add the values to the Exponential moving average to smooth them out a bit.
            # self._yaw_ema.add(self._yaw_riemann(time.time(), self._yaw_vel_riemann(time.time(), self._yaw_accel)))
            # self._pitch_ema.add(self._pitch_riemann(time.time(), self._pitch_vel_riemann(time.time(), self._pitch_accel)))
            # self._roll_ema.add(self._roll_riemann(time.time(), self._roll_vel_riemann(time.time(), self._roll_accel)))

            # Add the values to the Exponential moving average to smooth them out a bit.
            self._yaw_ema.add(self._yaw_integral.add_entry(self._yaw_vel_integral.add_entry(self._yaw_accel, time.time()), time.time()))
            self._pitch_ema.add(self._pitch_integral.add_entry(self._pitch_vel_integral.add_entry(self._pitch_accel, time.time()), time.time()))
            self._roll_ema.add(self._roll_integral.add_entry(self._roll_vel_integral.add_entry(self._roll_accel, time.time()), time.time()))

            self._yaw = self._yaw_ema.ema_value
            self._pitch = self._pitch_ema.ema_value
            self._roll = self._roll_ema.ema_value


            # print("Gyro:", int(self._yaw_ema.ema_value), int(self._pitch_ema.ema_value), int(self._roll_ema.ema_value), end=" | ")
            # print("Gyro:", round(self._yaw_ema.ema_value, 2), round(self._pitch_ema.ema_value, 2), round(self._roll_ema.ema_value, 2), end=" | ")

        if self.imuconfig.accel_name in imu.received_vals:
            accel = imu.received_vals[self.imuconfig.accel_name]

            # Combine the bytes.
            raw_x = accel['0'] | (accel['1'] << 8)
            raw_y = accel['2'] | (accel['3'] << 8)
            raw_z = accel['4'] | (accel['5'] << 8)

            # Make them signed again (2's compliment).
            signed_x = raw_x - 32768
            signed_y = raw_y - 32768
            signed_z = raw_z - 32768

            # Normalize the values to the +- g sensitivity setting we gave earlier.
            norm_x = signed_x * self._g / 32768
            norm_y = signed_y * self._g / 32768
            norm_z = signed_z * self._g / 32768

            # Subtract the offset values.
            self._accel_x = norm_x - self._x_offset
            self._accel_y = norm_y - self._y_offset
            self._accel_z = norm_z - self._z_offset

            # Add the values to the Exponential moving average to smooth them out a bit.
            self._accel_x_ema.add(self._accel_x)
            self._accel_y_ema.add(self._accel_y)
            self._accel_z_ema.add(self._accel_z)

            # print("Accel:", self._accel_x, self._accel_y, self._accel_z)

    def initialize_imu(self, imu: I2C) -> None:
        imu.sending_vals[self.imuconfig.gyro_init_register] = self.imuconfig.gyro_init_value
        imu.sending_vals[self.imuconfig.accel_init_register] = self.imuconfig.accel_init_value

    def calibrate_gyro(self) -> None:
        """Re-centers the gyroscope values. WARNING: Can cause unintended effects
        if not stationary when used."""
        self._yaw_offset += self._yaw_accel
        self._pitch_offset += self._pitch_accel
        self._roll_offset += self._roll_accel

        self._yaw_vel_integral.reset()
        self._pitch_vel_integral.reset()
        self._roll_vel_integral.reset()

        self._yaw_integral.reset()
        self._pitch_integral.reset()
        self._roll_integral.reset()
    
    def calibrate_accel(self) -> None:
        """Re-centers the gyroscope values. WARNING: Can cause unintended effects
        if not stationary when used."""
        self._x_offset += self._accel_x_ema.ema_value
        self._y_offset += self._accel_y_ema.ema_value
        self._z_offset += self._accel_z_ema.ema_value


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

    # @pitch.setter
    # def pitch(self, value):
    #     self._pitch = value


