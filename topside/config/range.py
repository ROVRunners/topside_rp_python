from typing import NamedTuple


class RangeConfig(NamedTuple):
    """Describes a range of values"""
    min: float
    max: float


class OptionalRangeConfig(NamedTuple):
    """Describes a range of values.  Either min or max can be None"""
    min: float | None
    max: float | None
