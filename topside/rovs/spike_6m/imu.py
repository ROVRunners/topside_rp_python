from time import time

from config.imu import IMUConfig
from hardware.i2c import I2C

from utilities.ema import EMA
from utilities.live_integration import Integration, IntegrationTypes
from utilities.vector import Vector3


class IMU:

    def __init__(self, imu_config: IMUConfig) -> None:
        """Initializes the IMU object.

        Args:
            imu_config (IMUConfig):
                The configuration for the IMU.
        """
        self._imu_config = imu_config

        int_type = IntegrationTypes.TRAPEZOIDAL

        self._yaw_vel_integral = Integration(int_type, 0, time(), False)
        self._pitch_vel_integral = Integration(int_type, 0, time(), False)
        self._roll_vel_integral = Integration(int_type, 0, time(), False)

        self._yaw_integral = Integration(int_type, 0, time(), False)
        self._pitch_integral = Integration(int_type, 0, time(), False)
        self._roll_integral = Integration(int_type, 0, time(), False)

        self._lateral_accel = Vector3(0.0, 0.0, 0.0)
        self._rotary_accel = Vector3(0.0, 0.0, 0.0)

        self._lateral_pos = Vector3(0.0, 0.0, 0.0)
        self._rotary_pos = Vector3(0.0, 0.0, 0.0)

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

        self._rotary_offset = Vector3(237, -122, -235)
        self._lateral_offset = Vector3(0, 0, 0)

    def update(self, imu: I2C) -> None:
        """Updates the yaw, pitch, roll, x, y, and z values

        Args:
            imu (I2C):
                The I2C object to get the values from.
        """
        if not imu.received_vals:
            return
        
        if self._imu_config.gyro_name in imu.received_vals:
            gyro = imu.received_vals[self._imu_config.gyro_name]

            # Combine the bytes.
            raw_rotary = Vector3(
                gyro['0'] | (gyro['1'] << 8),
                gyro['4'] | (gyro['5'] << 8),
                gyro['2'] | (gyro['3'] << 8)
            )

            # Make them signed again (2's compliment).
            signed_rotary: Vector3 = raw_rotary - 32768

            # Normalize the values to the +- dps sensitivity setting we gave earlier.
            norm_rotary: Vector3 = signed_rotary * self._dps / 32768

            # Subtract the offset values.
            self._rotary_accel = norm_rotary - self._rotary_offset

            # Add the values to the Exponential moving average to smooth them out a bit.
            self._yaw_ema.add(
                self._yaw_integral.add_entry(self._yaw_vel_integral.add_entry(
                    self._rotary_accel.yaw,
                    time()), time()
                )
            )
            self._pitch_ema.add(
                self._pitch_integral.add_entry(self._pitch_vel_integral.add_entry(
                    self._rotary_accel.pitch,
                    time()), time()
                )
            )
            self._roll_ema.add(
                self._roll_integral.add_entry(self._roll_vel_integral.add_entry(
                    self._rotary_accel.roll,
                    time()), time()
                )
            )

            self._rotary_pos = Vector3(self._yaw_ema.ema_value, self._pitch_ema.ema_value, self._roll_ema.ema_value)

        if self._imu_config.accel_name in imu.received_vals:
            accel = imu.received_vals[self._imu_config.accel_name]

            # Combine the bytes.
            raw_lateral = Vector3(
                accel['0'] | (accel['1'] << 8),
                accel['2'] | (accel['3'] << 8),
                accel['4'] | (accel['5'] << 8),
            )

            # Make them signed again (2's compliment).
            signed_lateral = raw_lateral - 32768

            # Normalize the values to the +- g sensitivity setting we gave earlier.
            norm_lateral = signed_lateral * self._g / 32768

            # Subtract the offset values.
            self._lateral_accel = norm_lateral - self._lateral_offset

            # Add the values to the Exponential moving average to smooth them out a bit.
            self._accel_x_ema.add(self._lateral_accel.x)
            self._accel_y_ema.add(self._lateral_accel.y)
            self._accel_z_ema.add(self._lateral_accel.z)

    def initialize_imu(self, imu: I2C) -> None:
        """Initializes the IMU with the given values in the IMUConfig class.

        Args:
            imu (I2C): The I2C object to send the values to.
        """
        imu.sending_vals[self._imu_config.gyro_init_register] = self._imu_config.gyro_init_value
        imu.sending_vals[self._imu_config.accel_init_register] = self._imu_config.accel_init_value

    def calibrate_gyro(self) -> None:
        """Re-centers the gyroscope values. WARNING: Can cause unintended effects
        if not stationary when used."""
        self._rotary_offset += self._rotary_accel

        self._yaw_vel_integral.reset()
        self._pitch_vel_integral.reset()
        self._roll_vel_integral.reset()

        self._yaw_integral.reset()
        self._pitch_integral.reset()
        self._roll_integral.reset()
    
    def calibrate_accel(self) -> None:
        """Re-centers the gyroscope values. WARNING: Can cause unintended effects
        if not stationary when used."""
        self._lateral_offset += self._lateral_accel

    @property
    def accel_x(self):
        return self._lateral_accel.x

    @property
    def accel_y(self):
        return self._lateral_accel.y

    @property
    def accel_z(self):
        return self._lateral_accel.z

    @property
    def yaw(self):
        return self._rotary_pos.yaw

    @property
    def roll(self):
        return self._rotary_pos.roll

    @property
    def pitch(self):
        return self._rotary_pos.pitch

    @property
    def rotary_pos(self):
        return self._rotary_pos

    @property
    def rotary_accel(self):
        return self._rotary_accel

    @property
    def lateral_pos(self):
        return self._lateral_pos

    @property
    def lateral_accel(self):
        return self._lateral_accel
