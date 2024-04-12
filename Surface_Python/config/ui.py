from typing import NamedTuple
from Surface_Python.utilities import color


class ColorConfig(NamedTuple):
    error_type_a: color.BACKGROUND_BLACK



class UIConfig(NamedTuple):
    color: ColorConfig

