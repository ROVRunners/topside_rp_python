from typing import NamedTuple


class LabelConfig(NamedTuple):
    name: str
    row: int
    column: int
    text: str
    rspan: int = 1
    cspan: int = 1


class ScaleConfig(NamedTuple):
    name: str
    row: int
    column: int
    min_: int
    max_: int
    default: int
    rspan: int = 1
    cspan: int = 1


class ImageConfig(NamedTuple):
    name: str
    row: int
    column: int
    width: int
    height: int
    filename: str
    rspan: int = 1
    cspan: int = 1

class DashboardConfig(NamedTuple):

    # Labels
    labels: tuple[LabelConfig, ...]

    # Slider bars
    scales: tuple[ScaleConfig, ...]

    # Orientation markers
    images: tuple[ImageConfig, ...]

    # Cameras
    # put_display("frame0", 1, 0, rspan=5)
    # put_display("frame1", 6, 0, rspan=5)


