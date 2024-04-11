"""A mapping between colors and escape codes for use in the text function"""

import os
import pkg_resources

# pylint: disable=wrong-import-position

# Initialization
DEPENDENCY = "colorama"
try:
    pkg_resources.require(DEPENDENCY)
except pkg_resources.DistributionNotFound:
    os.system(f'pip install {DEPENDENCY} --quiet')
    os.system(f'python -m pip install {DEPENDENCY} --quiet')
    os.system(f'python3 -m pip install {DEPENDENCY} --quiet')
    os.system(f'py -m pip install {DEPENDENCY} --quiet')

import colorama
colorama.init()

# _NAME means it does not work in VS Code.
# They weren't tested outside because that doesn't matter right now.

# Formatting
BOLD = '\033[1m'
_FAINT = '\033[2m'
ITALIC = '\033[3m'
UNDERLINE = '\033[4m'
_BLINKING = '\033[5m'
INVERSE = '\033[7m'
HIDDEN = '\033[8m'
STRIKETHROUGH = '\033[9m'

# Colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'

BRIGHT_BLACK = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_PURPLE = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'

DEFAULT_COLOR = '\033[39m'

# Background colors

BACKGROUND_BLACK = '\033[40m'
BACKGROUND_RED = '\033[41m'
BACKGROUND_GREEN = '\033[42m'
BACKGROUND_YELLOW = '\033[43m'
BACKGROUND_BLUE = '\033[44m'
BACKGROUND_PURPLE = '\033[45m'
BACKGROUND_CYAN = '\033[46m'
BACKGROUND_WHITE = '\033[47m'

BACKGROUND_BRIGHT_BLACK = '\033[100m'
BACKGROUND_BRIGHT_RED = '\033[101m'
BACKGROUND_BRIGHT_GREEN = '\033[102m'
BACKGROUND_BRIGHT_YELLOW = '\033[103m'
BACKGROUND_BRIGHT_BLUE = '\033[104m'
BACKGROUND_BRIGHT_PURPLE = '\033[105m'
BACKGROUND_BRIGHT_CYAN = '\033[106m'
BACKGROUND_BRIGHT_WHITE = '\033[107m'

BACKGROUND_DEFAULT_COLOR = '\033[49m'

# Specific use colors:

ERROR = '\033[38;2;255;140;25m'
PROMPT = CYAN
FILE_PRINT = PURPLE
GREET = BRIGHT_YELLOW
SUCCESS = BRIGHT_GREEN
FAIL = BRIGHT_RED
SEPERATOR = BLUE

# Symbols

WARN = "⚠ "

# Remove formatting

END = '\033[0m'


def custom(code: int, back: bool = False) -> str:
    """Give a text or background modification color code based off of a specific escape code.

    Args:
        code (int): The code of the desired modification.
        back (bool, optional):
            If True gives the code for modifying the background instead of the foreground.
            Defaults to False.

    Returns:
        str: The modification escape code ready to be input to text.
    """
    return f'\033[38;5;{code}m' if not back else f'\033[48;5;{code}m'


def rgb(red: int = 0, green: int = 0, blue: int = 0, back: bool = False) -> str:
    """Give a text or background modification color code based off of a decimal RGB input.

    Args:
        red (int, optional):
            Red value of the text (0-255).
            Defaults to 0.
        green (int, optional):
            Green value of the text (0-255).
            Defaults to 0.
        blue (int, optional):
            Blue value of the text (0-255).
            Defaults to 0.
        back (bool, optional):
            If True gives the code for modifying the background instead of the foreground.
            Defaults to False.

    Returns:
        str: The modification escape code ready to be input to text.
    """
    return (f'\033[38;2;{red};{green};{blue}m' if not back
            else f'\033[48;2;{red};{green};{blue}m')


def rgb_hex(red: str = 0, green: str = 0, blue: str = 0, back: bool = False) -> str:
    """Give a text or background modification color code based off of a hex RGB input.

    Args:
        red (str, optional):
            Red value of the text (00-FF).
            Defaults to 0.
        green (str, optional):
            Green value of the text (00-FF).
            Defaults to 0.
        blue (str, optional):
            Blue value of the text (00-FF).
            Defaults to 0.
        back (bool, optional):
            If True gives the code for modifying the background instead of the foreground.
            Defaults to False.

    Returns:
        str: The modification escape code ready to be input to text.
    """
    return (f'\033[38;2;{int(red, 16)};{int(green, 16)};{int(blue, 16)}m' if not back
            else f'\033[48;2;{red};{green};{blue}m')
