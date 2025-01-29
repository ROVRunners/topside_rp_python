import os
import sys

rov_name = ""
current_directory = os.path.dirname(os.path.realpath(__file__))
with open(f"{current_directory}/launch_config.fngr", "r") as file:
    file_lines = file.readlines()[:]
    for line in file_lines:
        # Skip empty lines and comments.
        if not line.strip() or line.strip().startswith("#"):
            continue

        # Check for the rov_name.
        if "rov_name" == line.lower().split("=")[0].strip():
            rov_name = line.split("=")[1].strip()
            break

if not rov_name:
    raise Exception("rov_name not found in launch_config.fngr")

# Add the rov_name to the path so that we can import the correct rov files.
sys.path.append(os.path.join(os.path.join(current_directory, "rovs"), rov_name))

import surface_main

import utilities.personal_functions as pf


# Set to True to enable debug mode, which will crash the program on exceptions.
debug: bool = True


def run():

    main_system = surface_main.MainSystem()

    while main_system.run:
        # If debug is enabled, we want to hit exceptions so that we can see them.
        if debug:
            try:
                main_system.main_loop()
            except KeyboardInterrupt as e:
                pf.error(f'KeyboardInterrupt in main_system.main_loop():\n{e}')
                main_system.shutdown()
        # If debug is disabled, we want to catch exceptions so that the program doesn't crash.
        else:
            try:
                main_system.main_loop()
            except Exception as e:
                pf.error(f'Exception in main_system.main_loop():\n{e}')


if __name__ == "__main__":
    run()
