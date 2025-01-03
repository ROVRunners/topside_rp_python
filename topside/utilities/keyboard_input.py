"""Work with keyboard inputs."""
# Disables annoying and usually incorrect warnings.
# pylint: disable=wrong-import-position
# pylint: disable=import-error

import os
# import pkg_resources
#
# # Checks to see if the dependency is installed. If not, installs it.
# DEPENDENCY = "keyboard"
# try:
#     pkg_resources.require(DEPENDENCY)
# except pkg_resources.DistributionNotFound:
#     os.system(f'pip install {DEPENDENCY} --quiet')
#     os.system(f'python -m pip install {DEPENDENCY} --quiet')
#     os.system(f'python3 -m pip install {DEPENDENCY} --quiet')
#     os.system(f'py -m pip install {DEPENDENCY} --quiet')

import keyboard

# The keys previously pressed
keys = {}


def is_newly_pressed(key: str, function: callable or None = None) -> bool:
    """Detect if a key is pressed and return True if
    it wasn't pressed the last time this function was called.
    Designed to be run every frame.

    Args:
        key (str): 
             key to check the newness of the compression thereof.
        function (str, optional): 
             The function to execute if the key is newly pressed.

    Returns:
        bool: True if the key is pressed but was not pressed during the previous call.
        False otherwise.
    """
    result = False

    # If the key has been pressed previously, check it's previous value.
    # If it says it wasn't pressed, but it is now, change to fit and set the result accordingly
    # and vise-versa.
    # If the current and previous values are the same, set the result to False.
    if key in keys:
        if keyboard.is_pressed(key) and keys[key] is False:
            keys[key] = True
            result = True
        elif keyboard.is_pressed(key) and keys[key] is True:
            pass
        else:
            keys[key] = False

    # If it isn't in the list, set the result and the value
    # to whether or not it's currently pressed.
    else:
        if keyboard.is_pressed(key):
            keys[key] = True
            result = True
        else:
            keys[key] = False

    # If a function is provided and the result was True, run the function.
    if result and function is not None:
        function()

    return result


def is_currently_pressed(key: str, function: callable or None = None) -> bool:
    """Check to see if a key is currently pressed.

    Args:
        key (str): The key to check.
        function (callable | None, optional):
            The function to call if the key is pressed.
            Defaults to None.

    Returns:
        bool: True if the key is pressed. False otherwise.
    """
    # Update the list
    keys[key] = keyboard.is_pressed(key)

    # Run if true
    if function is not None and keys[key] is True:
        function()

    return keys[key]
