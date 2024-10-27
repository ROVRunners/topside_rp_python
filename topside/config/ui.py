from typing import NamedTuple
from topside.utilities import color


class ColorConfig(NamedTuple):
    error: [color.ERROR, color.BACKGROUND_YELLOW, color.UNDERLINE, color.BOLD, color.WARN]
    warning: [color.BRIGHT_YELLOW, color.UNDERLINE, color.WARN]
    success: [color.BRIGHT_GREEN]
    info: [color.BRIGHT_BLUE]
    debug: [color.BRIGHT_PURPLE]
    normal: [color.DEFAULT_COLOR]
    prompt: [color.BRIGHT_CYAN]


class StringConfig(NamedTuple):
    prompt_string: str = ">>> "
    error_string: str = color.WARN + "ERROR: "
    warning_string: str = color.WARN + "WARNING: "
    success_string: str = "SUCCESS: "
    info_string: str = "INFO: "
    debug_string: str = "DEBUG: "
    normal_string: str = ""


class UIConfig(NamedTuple):
    color: ColorConfig
    string: StringConfig

