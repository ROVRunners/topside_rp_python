from typing import NamedTuple

class PIDConfig(NamedTuple):
    """Describe a pid configuration (p, i, d)"""
    p: float = 0
    i: float = 0
    d: float = 0