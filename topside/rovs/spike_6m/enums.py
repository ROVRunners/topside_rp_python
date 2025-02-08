"""Declaration of enums used in the configuration of the ROV."""

import enum


# TODO: Make this accurate.
class MavlinkMessageTypes(enum.Enum):
    HEARTBEAT = 0
    SYS_STATUS = 1
    SYSTEM_TIME = 2
    PING = 4
    CHANGE_OPERATOR_CONTROL = 5
    CHANGE_OPERATOR_CONTROL_ACK = 6
    AUTH_KEY = 7
    SET_MODE = 11
    PARAM_REQUEST_READ = 20
    PARAM_REQUEST_LIST = 21
    PARAM_VALUE = 22
    PARAM_SET = 23
    GPS_RAW_INT = 24
    GPS_STATUS = 25
    SCALED_IMU = 26
    RAW_IMU = 27
    RAW_PRESSURE = 28
    SCALED_PRESSURE = 29
    ATTITUDE = 30
    ATTITUDE_QUATERNION = 31
    LOCAL_POSITION_NED = 32
    GLOBAL_POSITION_INT = 33
    RC_CHANNELS_SCALED = 34
    RC_CHANNELS_RAW = 35
    SERVO_OUTPUT_RAW = 36
    MISSION_REQUEST_PARTIAL_LIST = 37
    MISSION_WRITE_PARTIAL_LIST = 38
    MISSION_ITEM = 39
    MISSION_REQUEST = 40
    MISSION_SET_CURRENT = 41
    MISSION_CURRENT = 42
    MISSION_REQUEST_LIST = 43
    MISSION_COUNT = 44
    MISSION_CLEAR_ALL = 45
    MISSION_ITEM_REACHED = 46
    MISSION_ACK = 47
    SET_GPS_GLOBAL_ORIGIN = 48
    GPS_GLOBAL_ORIGIN = 49
    PARAM_MAP_RC = 50
    MISSION_REQUEST_INT = 51
    SAFETY_SET_ALLOWED_AREA = 54
    SAFETY_ALLOWED_AREA = 55
    ATTITUDE_QUATERNION_COV = 61
    NAV_CONTROLLER_OUTPUT = 62
    GLOBAL_POSITION_INT_COV = 63
    LOCAL_POSITION_NED_COV = 64
    RC_CHANNELS = 65
    REQUEST_DATA_STREAM = 66
    DATA_STREAM = 67
    MANUAL_CONTROL = 69
    RC_CHANNELS_OVERRIDE = 70
    MISSION_ITEM_INT = 73
    VFR_HUD = 74
    COMMAND_INT = 75
    COMMAND_LONG = 76
    COMMAND_ACK = 77
    MANUAL_SETPOINT = 81
    SET_ATTITUDE_TARGET = 82
    ATTITUDE_TARGET = 83
    SET_POSITION_TARGET_LOCAL_NED = 84
    POSITION_TARGET_LOCAL_NED = 85
    SET_POSITION_TARGET_GLOBAL_INT = 86
    POSITION_TARGET_GLOBAL_INT = 87
    LOCAL_POSITION_NED_SYSTEM_GLOBAL_OFFSET = 89
    HIL_STATE = 90
    HIL_CONTROLS = 91
    HIL_RC_INPUTS_RAW = 92
    HIL_ACTUATOR_CONTROLS = 93
    OPTICAL_FLOW = 100
    GLOBAL_VISION_POSITION_ESTIMATE = 101
    VISION_POSITION_ESTIMATE = 102
    VISION_SPEED_ESTIMATE = 103
    VICON_POSITION_ESTIMATE = 104
    HIGHRES_IMU = 105
    OPTICAL_FLOW_RAD = 106
    HIL_SENSOR = 107
    SIM_STATE = 108
    RADIO_STATUS = 109
    FILE_TRANSFER_PROTOCOL = 110
    TIMESYNC = 111
    CAMERA_TRIGGER = 112
    HIL_GPS = 113
    HIL_OPTICAL_FLOW = 114
    HIL_STATE_QUATERNION = 115
    SCALED_IMU2 = 116
    LOG_REQUEST_LIST = 117
    LOG_ENTRY = 118
    LOG_REQUEST_DATA = 119
    LOG_DATA = 120
    LOG_ERASE = 121
    LOG_REQUEST_END = 122
    GPS_INJECT_DATA = 123
    GPS2_RAW = 124
    POWER_STATUS = 125
    SERIAL_CONTROL = 126
    GPS_RTK = 127
    GPS2_RTK = 128
    SCALED_IMU3 = 129
    DATA_TRANSMISSION_HANDSHAKE = 130
    ENCAPSULATED_DATA = 131
    DISTANCE_SENSOR = 132
    TERRAIN_REQUEST = 133
    TERRAIN_DATA = 134
    TERRAIN_CHECK = 135
    TERRAIN_REPORT = 136
    SCALED_PRESSURE2 = 137
    ATT_POS_MOCAP = 138
    SET_ACTUATOR_CONTROL_TARGET = 139
    ACTUATOR_CONTROL_TARGET = 140
    ALTITUDE = 141
    RESOURCE_REQUEST = 142
    SCALED_PRESSURE3 = 143
    FOLLOW_TARGET = 144
    CONTROL_SYSTEM_STATE = 146
    BATTERY_STATUS = 147
    AUTOPILOT_VERSION = 148
    LANDING_TARGET = 149
    ESTIMATOR_STATUS = 230
    WIND_COV = 231
    GPS_INPUT = 232
    GPS_RTCM_DATA = 233
    HIGH_LATENCY = 234
    HIGH_LATENCY2 = 235
    MAV_CMD_PREFLIGHT_CALIBRATION = 241
    HOME_POSITION = 242
    SET_HOME_POSITION = 243
    MESSAGE_INTERVAL = 244
    EXTENDED_SYS_STATE = 245
    ADSB_VEHICLE = 246
    COLLISION = 247
    V2_EXTENSION = 248
    MEMORY_VECT = 249
    DEBUG_VECT = 250
    NAMED_VALUE_FLOAT = 251
    NAMED_VALUE_INT = 252
    STATUSTEXT = 253
    DEBUG = 254
    SETUP_SIGNING = 256
    BUTTON_CHANGE = 257
    PLAY_TUNE = 258
    CAMERA_INFORMATION = 259
    CAMERA_SETTINGS = 260
    STORAGE_INFORMATION = 261
    CAMERA_CAPTURE_STATUS = 262
    CAMERA_IMAGE_CAPTURED = 263
    FLIGHT_INFORMATION = 264
    MOUNT_ORIENTATION = 265
    LOGGING_DATA = 266
    LOGGING_DATA_ACKED = 267
    LOGGING_ACK = 268


# Define the Buttons and Axes
class ControllerAxisNames(enum.StrEnum):
    """The axes available on the controller.

    Implements:
        enum.StrEnum

    Properties:
        LEFT_X (str):
            The left x-axis of the controller.
        LEFT_Y (str):
            The left y-axis of the controller.
        RIGHT_X (str):
            The right x-axis of the controller.
        RIGHT_Y (str):
            The right y-axis of the controller.
        LEFT_TRIGGER (str):
            The left trigger of the controller.
        RIGHT_TRIGGER (str):
            The right trigger of the controller.
    """
    LEFT_X = "LEFT_X",
    LEFT_Y = "LEFT_Y",
    RIGHT_X = "RIGHT_X",
    RIGHT_Y = "RIGHT_Y",
    LEFT_TRIGGER = "LEFT_TRIGGER",
    RIGHT_TRIGGER = "RIGHT_TRIGGER",

    def __repr__(self):
        return self.value


class ControllerButtonNames(enum.StrEnum):
    """The buttons available on the controller.

    Implements:
        enum.StrEnum

    Properties:
        A (str):
            The A button on the controller.
        B (str):
            The B button on the controller.
        X (str):
            The X button on the controller.
        Y (str):
            The Y button on the controller.
        START (str):
            The start button on the controller.
        SELECT (str):
            The select button on the controller.
        LEFT_BUMPER (str):
            The left bumper on the controller.
        RIGHT_BUMPER (str):
            The right bumper on the controller.
    """
    A = "A",
    B = "B",
    X = "X",
    Y = "Y",
    START = "START",
    SELECT = "SELECT",
    LEFT_BUMPER = "LEFT_BUMPER",
    RIGHT_BUMPER = "RIGHT_BUMPER",

    def __repr__(self):
        return self.value


class ControllerHatNames(enum.StrEnum):
    """The D-Pad available on the controller.

    Implements:
        enum.StrEnum

    Properties:
        DPAD (str):
            The only D-Pad on the controller in this configuration.
    """
    DPAD = "DPAD",

    def __repr__(self):
        return self.value


class ControllerHatButtonNames(enum.StrEnum):
    """The D-Pad directions available on the controller.

    Implements:
        enum.StrEnum

    Properties:
        DPAD_UP (str):
            The up direction on the D-Pad.
        DPAD_DOWN (str):
            The down direction on the D-Pad.
        DPAD_LEFT (str):
            The left direction on the D-Pad.
        DPAD_RIGHT (str):
            The right direction on the D-Pad.
    """
    DPAD_UP = "DPAD_UP",
    DPAD_DOWN = "DPAD_DOWN",
    DPAD_LEFT = "DPAD_LEFT",
    DPAD_RIGHT = "DPAD_RIGHT",

    def __repr__(self):
        return self.value


class ControllerNames(enum.StrEnum):
    """The names of the controllers available.

    Implements:
        enum.StrEnum

    Properties:
        PRIMARY_DRIVER (str):
            The only driver controller in this configuration.
    """
    PRIMARY_DRIVER = "PRIMARY_DRIVER",

    def __repr__(self):
        return self.value


# Define the Thrusters and Orientations
class ThrusterPositions(enum.StrEnum):
    """The thrusters and associated names available to this ROV.

    Implements:
        enum.StrEnum

    Properties:
        FRONT_RIGHT (str):
            The front right thruster.
        FRONT_LEFT (str):
            The front left thruster.
        REAR_RIGHT (str):
            The rear right thruster.
        REAR_LEFT (str):
            The rear left thruster.
        FRONT_VERTICAL (str):
            The front vertical thruster.
        REAR_VERTICAL (str):
            The rear vertical thruster.
    """
    FRONT_RIGHT = "FRONT_RIGHT",
    FRONT_LEFT = "FRONT_LEFT",
    REAR_RIGHT = "REAR_RIGHT",
    REAR_LEFT = "REAR_LEFT",
    FRONT_VERTICAL = "FRONT_VERTICAL",
    REAR_VERTICAL = "REAR_VERTICAL",

    def __repr__(self):
        return self.value


class Directions(enum.StrEnum):
    """The directions that thrusters can apply force in.

    Implements:
        enum.StrEnum

    Properties:
        FORWARDS (str):
            The force a thruster generates in the forwards direction.
        RIGHT (str):
            The force a thruster generates in the right direction.
        UP (str):
            The force a thruster generates in the up direction.
        YAW (str):
            The force a thruster generates in the clockwise yaw axis.
        PITCH (str):
            The force a thruster generates in the pitch axis (front tipping up).
        ROLL (str):
            The force a thruster generates in the roll axis (left side tipping up).
    """
    FORWARDS = "FORWARDS",
    RIGHT = "RIGHT",
    UP = "UP",
    YAW = "YAW",
    PITCH = "PITCH",
    ROLL = "ROLL",

    def __repr__(self):
        return self.value


class ControlModes(enum.StrEnum):
    """The control modes available to the ROV.

    Implements:
        enum.StrEnum

    Properties:
        MANUAL (str):
            The manual control mode.
        PID_TUNING (str):
            The PID tuning mode.
        TESTING (str):
            The testing mode.
        DEPTH_HOLD (str):
            The depth hold mode.
        HEADING_HOLD (str):
            The heading hold mode.
        POSITION_HOLD (str):
            The position hold mode.
        FULL_PID (str):
            The full PID control mode.
    """
    MANUAL = "MANUAL",
    PID_TUNING = "PID_TUNING",
    TESTING = "TESTING",
    DEPTH_HOLD = "DEPTH_HOLD",
    HEADING_HOLD = "HEADING_HOLD",
    POSITION_HOLD = "POSITION_HOLD",
    FULL_PID = "FULL_PID",

    def __repr__(self):
        return self.value
