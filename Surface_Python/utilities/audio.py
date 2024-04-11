"""Audio settings"""
# Disables annoying and usually incorrect warnings.
# pylint: disable=wrong-import-position
# pylint: disable=import-error
# pylint: disable=no-member

import os
import pkg_resources

# Checks to see if the dependency is installed. If not, installs it.
DEPENDENCY = "pygame"
try:
    pkg_resources.require(DEPENDENCY)
except pkg_resources.DistributionNotFound:
    os.system(f'pip install {DEPENDENCY} --quiet')
    os.system(f'python -m pip install {DEPENDENCY} --quiet')
    os.system(f'python3 -m pip install {DEPENDENCY} --quiet')
    os.system(f'py -m pip install {DEPENDENCY} --quiet')

import pygame

# Initialize Pygame
pygame.init()

# Set the volume (optional)
pygame.mixer.music.set_volume(0.5)  # Sets volume to 50%


def play_background(file: str, loops: int = 1, start: float = 0, fade_ms: int = 0) -> None:
    """Play music in the background (simultaneously to code).

    Args:
        file (str): The path to the audio.
        loops (int, optional):
            The number of times to loop the file. Entering -1 makes it loop infinitely.
            Defaults to 1.
        start (float, optional):
            The start time, I assume (untested).
            Defaults to 1.
        fade_ms (int, optional):
            The fade time, I assume (untested).
            Defaults to 1.
    """
    stop_music()

    pygame.mixer.music.load(file, file)

    pygame.mixer.music.play(loops, start, fade_ms)


def stop_music() -> None:
    """Stop any playing music."""
    pygame.mixer.music.stop()


def set_volume(volume: float) -> None:
    """Change the volume of any playing music."""
    pygame.mixer.music.set_volume(volume)
