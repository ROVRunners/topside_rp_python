'''
test mavlink messages
'''
from __future__ import print_function

from pymavlink import mavutil


def wait_heartbeat(m):
    """Wait for a heartbeat so we can know the target system IDs."""
    print("Waiting for APM heartbeat")
    msg = m.recv_match(type='HEARTBEAT', blocking=True)
    print(msg)
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_component))


# create a mavlink serial instance
master = mavutil.mavlink_connection("COM11", baud=115200, source_system=255)


# # Request all sensor data
# # The parameters are:
# # - target_system: 0 means all systems
# # - target_component: 0 means all components
# # - req_stream_id: 0 for all streams
# # - req_message_rate: 1 for 1 Hz (you can adjust this)
# # - start_stop: 1 to start sending data
# master.mav.command_long_send(
#     master.target_system,
#     master.target_component,
#     mavutil.mavlink.MAV_CMD_REQUEST_DATA_STREAM,
#     0,  # confirmation
#     0,  # request all streams
#     1,  # request rate (1 Hz)
#     0,  # start/stop (1 to start)
#     0, 0, 0, 0  # unused parameters
# )


# Set the message interval for SENSOR_DATA (message ID 147) to 1 Hz (1000000 microseconds)
message_id = 26  # Change this to the desired message ID
interval = 1000000  # Interval in microseconds (1 second)

off = False

if off:
    interval *= 0

# master.mav.command_long_send(
#     master.target_system,
#     master.target_component,
#     mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
#     # 0,  # confirmation
#     0,
#     message_id,  # message ID
#     interval,  # interval in microseconds
#     message_id,  # unused parameter
#     0, 0, 0, 0  # unused parameters
# )

# for I in range(255):
#     # Send the command to set the message interval
#     master.mav.command_long_send(
#         master.target_system,
#         master.target_component,
#         mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
#         0,  # confirmation
#         I,  # message ID for RAW_IMU
#         interval,  # interval in microseconds
#         0,  # unused parameter
#         0, 0, 0, 0  # unused parameters
#     )
# Send the command to set the message interval
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0,  # confirmation
    message_id,  # message ID for RAW_IMU
    interval,  # interval in microseconds
    0,  # unused parameter
    0, 0, 0, 0  # unused parameters
)

# wait for the heartbeat msg to find the system ID
# wait_heartbeat(master)
message_type_dict = {}

while True:
    msg = master.recv_match(type="SCALED_IMU", blocking=True)
    message_type_dict[msg.get_type()] = msg.to_dict()
    print(msg)
