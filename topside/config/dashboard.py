from typing import NamedTuple


class LabelConfig(NamedTuple):
    """A configuration for a label on the dashboard.

    Attributes:
        name (str): The name of the label.
        row (int): The row of the label.
        column (int): The column of the label.
        text (str): The text of the label.
        rspan (int): The number of rows spanned by the label.
        cspan (int): The number of columns spanned by the label.
    """
    name: str
    row: int
    column: int
    text: str
    rspan: int = 1
    cspan: int = 1


class ScaleConfig(NamedTuple):
    """A configuration for a slider bar on the dashboard.

    Attributes:
        name (str): The name of the slider bar.
        row (int): The row of the slider bar.
        column (int): The column of the slider bar.
        min_ (int): The minimum value of the slider bar.
        max_ (int): The maximum value of the slider bar.
        default (int): The default value of the slider bar.
        rspan (int): The number of rows spanned by the slider bar.
        cspan (int): The number of columns spanned by the slider bar.
    """
    name: str
    row: int
    column: int
    min_: int
    max_: int
    default: int
    rspan: int = 1
    cspan: int = 1


class ImageConfig(NamedTuple):
    """A configuration for an image on the dashboard.

    Attributes:
        name (str): The name of the image.
        row (int): The row of the image.
        column (int): The column of the image.
        width (int): The width of the image.
        height (int): The height of the image.
        filename (str): The filename of the image.
        rspan (int): The number of rows spanned by the image.
        cspan (int): The number of columns spanned by the image.
    """
    name: str
    row: int
    column: int
    width: int
    height: int
    filename: str
    rspan: int = 1
    cspan: int = 1


class DashboardConfig(NamedTuple):
    """A configuration for a dashboard.

    Attributes:
        labels (tuple[LabelConfig, ...]): The labels on the dashboard.
        scales (tuple[ScaleConfig, ...]): The slider bars on the dashboard.
        images (tuple[ImageConfig, ...]): The orientation markers on the dashboard.
    """

    # Labels
    labels: tuple[LabelConfig, ...]

    # Slider bars
    scales: tuple[ScaleConfig, ...]

    # Orientation markers
    images: tuple[ImageConfig, ...]

    # Cameras
    # put_display("frame0", 1, 0, rspan=5)
    # put_display("frame1", 6, 0, rspan=5)
