import thruster_pwm


class ROVConfig:
    """Class for the ROV configuration."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""
        # Purely informational data.
        self.system_info: dict = {
            "rov_name": "Spike the Lionfish",
            "date": "4/13/2024",
            "team_name": "LBCC ROVRunners",
            "rov_description": "The main ROV for the LBCC ROVRunners team.",
            "rov_type": "ROV",
            "rov_id": "0",
            "rov_serial_number": "0001",
            "rov_version": "0.1.0",
            "rov_max_speed": "N/A m/s",
            "rov_max_depth": "N/A m",
            "rov_max_runtime": "60 minutes",
            "rov_power_rating": "48V",
            "rov_power_supply": "Tether",
            "rov_control_method": "Xbox Controller",
            "rov_internal_communication": "Serial",
            "rov_navigation": "IMU",  # Other options: "GPS", "Sonar"
            "rov_sensors": ["Depth", "Temperature", "Pressure"],
            "rov_digital_cameras": ["N/A"],
            "rov_analog_cameras": ["N/A"],
            "rov_lights": ["N/A"],
            "rov_manipulators": ["Claw", "Rotator"],
            "rov_payload": "N/A",
            "rov_status": "Not Operational -- Assembly phase",
        }
        # Used for controller I/O.
        self.controller_info: dict = {
            "controller_type": "Xbox Controller",
            "controller_model": "Xbox One",
            "controller_connection": "USB",
            "controller_status": "Operational",
        }
        # Used for sensor I/O.
        self.sensor_info: dict = {
            "depth": {
                "sensor_type": "Pressure",
                "sensor_model": "MS5837-30BA",
                "sensor_range": "0-30 bar",
                "sensor_resolution": "0.2 mbar",
                "sensor_accuracy": "0.01% FS",
                "sensor_output": "I2C",
                "sensor_status": "Operational",
            },
            "temperature": {
                "sensor_type": "Temperature",
                "sensor_model": "MS5837-30BA",
                "sensor_range": "-40 to 85 C",
                "sensor_resolution": "0.01 C",
                "sensor_accuracy": "0.2 C",
                "sensor_output": "I2C",
                "sensor_status": "Operational",
            },
            "pressure": {
                "sensor_type": "Pressure",
                "sensor_model": "MS5837-30BA",
                "sensor_range": "0-30 bar",
                "sensor_resolution": "0.2 mbar",
                "sensor_accuracy": "0.01% FS",
                "sensor_output": "I2C",
                "sensor_status": "Operational",
            },

        }

        # Used for motor I/O.
        self.motor_info: dict = {
            "motor_fv": {
                "type": "Brushless DC",
                "model": "T200",
                "max_thrust_fwd": "6.7 kg force",
                "max_thrust_rev": "5.05 kg force",
                "max_current": "32A",
                "voltage_rating": "7-20V",
                "pwm_full_reverse": "1100",
                "pwm_stop": "1500",
                "pwm_full_forward": "1900",
                "status": "Operational",
            },
            "motor_rv": {
                "type": "Brushless DC",
                "model": "T200",
                "max_thrust_fwd": "6.7 kg force",
                "max_thrust_rev": "5.05 kg force",
                "max_current": "32A",
                "voltage_rating": "7-20V",
                "pwm_full_reverse": "1100",
                "pwm_stop": "1500",
                "pwm_full_forward": "1900",
                "status": "Operational",
            },
            "motor_fr": {
                "type": "Brushless DC",
                "model": "T200",
                "max_thrust_fwd": "6.7 kg force",
                "max_thrust_rev": "5.05 kg force",
                "max_current": "32A",
                "voltage_rating": "7-20V",
                "pwm_full_reverse": "1100",
                "pwm_stop": "1500",
                "pwm_full_forward": "1900",
                "status": "Operational",
            },
            "motor_fl": {
                "type": "Brushless DC",
                "model": "T200",
                "max_thrust_fwd": "6.7 kg force",
                "max_thrust_rev": "5.05 kg force",
                "max_current": "32A",
                "voltage_rating": "7-20V",
                "pwm_full_reverse": "1100",
                "pwm_stop": "1500",
                "pwm_full_forward": "1900",
                "status": "Operational",
            },
            "motor_rr": {
                "type": "Brushless DC",
                "model": "T200",
                "max_thrust_fwd": "6.7 kg force",
                "max_thrust_rev": "5.05 kg force",
                "max_current": "32A",
                "voltage_rating": "7-20V",
                "pwm_full_reverse": "1100",
                "pwm_stop": "1500",
                "pwm_full_forward": "1900",
                "status": "Operational",
            },
            "motor_rl": {
                "type": "Brushless DC",
                "model": "T200",
                "max_thrust_fwd": "6.7 kg force",
                "max_thrust_rev": "5.05 kg force",
                "max_current": "32A",
                "voltage_rating": "7-20V",
                "pwm_full_reverse": "1100",
                "pwm_stop": "1500",
                "pwm_full_forward": "1900",
                "status": "Operational",
            },
            # "motor_configuration": {
            #     "motor_configuration": { # X | Y | Orientation
            #         "motor_fv": "Center | Front |  Up",
            #         "motor_rv": "Center | Rear  | Down",
            #         "motor_fr": "Right  | Front | Rear/Right",
            #         "motor_fl": " Left  | Front | Front/Right",
            #         "motor_rr": "Right  | Rear  | Right",
            #         "motor_rl": " Left  | Rear  | Right",
            #     },
            # },
        }
        # Purely informational data.
        self.camera_info: dict = {
            "forward": {
                "type": "Digital",
                "model": "N/A",
                "resolution": "N/A mp",
                "fov": "N/A degrees",
                "status": "N/A",
            },
        }
        # Purely informational data.
        self.light_info: dict = {
            "forward_light": {
                "type": "N/A",
                "model": "N/A",
                "intensity": "N/A lumens",
                "status": "N/A",
            },
        }
        # Purely informational data.
        self.manipulator_info: dict = {
            "claw": {
                "type": "Claw",
                "model": "Custom",
                "actuator": "2x Solenoid",
                "status": "N/A",
            },
            "rotator": {
                "type": "Rotator",
                "model": "Custom",
                "actuator": "1x Solenoid",
                "status": "N/A",
            },
        }
        # Purely informational data.
        self.payload_info: dict = {
            "type": "N/A",
            "model": "N/A",
            "status": "Not planned",
        }
        # Purely informational data.
        self.navigation_info: dict = {
            "type": "Flight Controller",
            "model": "Pixhawk 6c",
            "status": "Not Operational -- Planned",
        }
        # Purely informational data.
        self.buoyancy_info: dict = {
            "type": "Foam Blocks",
            "model": "Custom",
            "status": "Not Operational -- Assembly phase",
        }
        # Purely informational data.
        self.system_status: dict = {
            "rov_status": "Not Operational -- Assembly phase",
            "controller_status": "Operational",
            "sensor_status": "Not Operational -- Planned",
            "motor_status": "Operational",
            "camera_status": "Not Operational -- Planned",
            "light_status": "Not planned",
            "manipulator_status": "Not Operational -- Assembly phase",
            "buoyancy_status": self.buoyancy_info["status"],
            "payload_status": "Not planned",
            "navigation_status": self.navigation_info["status"],
        }
        # Purely informational data.
        self.system_errors: dict = {
            "rov_errors": "None",
            "controller_errors": "None",
            "sensor_errors": "None",
            "motor_errors": "None",
            "camera_errors": "None",
            "light_errors": "None",
            "manipulator_errors": "None",
            "buoyancy_errors": "None",
            "payload_errors": "None",
            "navigation_errors": "None",
        }
        # Purely informational data.
        self.system_warnings: dict = {
            "rov_warnings": "None",
            "controller_warnings": "None",
            "sensor_warnings": "None",
            "motor_warnings": "None",
            "camera_warnings": "None",
            "light_warnings": "None",
            "manipulator_warnings": "None",
            "buoyancy_warnings": "None",
            "payload_warnings": "None",
            "navigation_warnings": "None",
        }
        # Purely informational data.
        self.system_notes: dict = {
            "rov_notes": "None",
            "controller_notes": "None",
            "sensor_notes": "None",
            "motor_notes": "None",
            "camera_notes": "None",
            "light_notes": "None",
            "manipulator_notes": "None",
            "buoyancy_notes": "None",
            "payload_notes": "None",
            "navigation_notes": "None",
        }

        # Operational data.
        self.pwm_conversion_function = thruster_pwm.get_pwm_values
        self.stationary_pwm_values = [1500, 1500, 1500, 1500, 1500, 1500]
        self.motor_thrust_multipliers = [.8, .8, .8, .8, .8, .8]

