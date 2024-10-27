"""This module contains functions for handling input data and controlling the ROV.

The `process_gamepad_input` function processes gamepad input data and controls the ROV thrusters accordingly.
The `process_command_input` function processes command input and returns a response.
The `get_status` function retrieves the current status of the ROV.
"""
from topside.rov_config.spike import rov_config


# class ROVClass:
#     """Basic class for an ROV used primarily for data storage."""
#     def __init__(self, thrusters, mode, temperature, pressure, depth, leak_detected, armed):
#         self.thrusters = thrusters
#         self.mode = mode
#         self.temperature = temperature
#         self.pressure = pressure
#         self.depth = depth
#         self.leak_detected = leak_detected
#         self.armed = armed
#
#
# rov = ROVClass(thrusters=[0, 0, 0, 0, 0, 0], mode="Manual", temperature="69",
#                pressure="N/A", depth="N/A", leak_detected=-1, armed=False)


# def process_gamepad_input(data):
#     """
#     Process the gamepad input data and control the ROV thrusters accordingly.
#
#     Args:
#         data (dict): A dictionary containing the gamepad input data,
#                         including 'x', 'y', and 'r' values.
#
#     Returns:
#         str: A response indicating that the gamepad input has been received.
#     """
#
#     print(data)
#
#     if rov.armed:
#
#         # TODO Handle buttons and triggers
#
#     return "Gamepad input received"


# def process_command_input(command: str) -> str:
#     """Process the command input and return a response.
#
#     Args:
#         command (str): The command input to be processed.
#
#     Returns:
#         str: The response message.
#     """
#
#     command = command.lower().strip()
#     response = "Command received: " + command + ".</br>"
#
#     if command == "arm":
#         rov.armed = True
#         response += "ROV armed."
#
#     elif command == "clear":
#         response = ""
#
#     elif command == "disarm":
#         rov.armed = False
#         response += "ROV disarmed."
#
#     elif command == "help":
#         response += """Available commands:
#                         </br>arm: Allow control inputs.
#                         </br>clear: Clear the console log.
#                         </br>disarm: Disallow control inputs.
#                         </br>help: Display this help message.
#                         """
#
#     else:
#         response += "Invalid command. Type 'help' for a list of available commands."
#
#     return response


# def get_status():
#     """Retrieves the current status of the ROV.
#
#     Returns:
#         dict: A dictionary containing the following status information:
#             - "armed" (bool): Indicates whether the ROV is armed.
#             - "mode" (str): The current mode of the ROV.
#             - "depth" (str): The current depth of the ROV in meters.
#             - "temperature" (str): The current temperature of the ROV in degrees Celsius.
#             - "pressure" (str): The current pressure around the ROV in millibars.
#             - "leak_detected" (bool): Indicates whether a leak has been detected.
#             - "thrusters" (list): A list of thruster information.
#     """
#     status = {
#         "armed": rov.armed,
#         "mode": rov.mode,
#         "depth": rov.depth + "m",
#         "temperature": rov.temperature + "°C",
#         "pressure": rov.pressure + "PSI",
#         "leak_detected": rov.leak_detected,
#         "thrusters": rov.thrusters
#     }
#
#     return status
