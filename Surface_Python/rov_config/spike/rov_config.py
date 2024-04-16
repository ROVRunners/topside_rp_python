import manual
import auto
import rov_info


class ROVConfig:
    """Class for the ROV configuration."""

    def __init__(self) -> None:
        """Initialize an instance of the class."""

        # All the following values except the manual class and intercepts
        # can be either filled or set to None, but they MUST be defined.

        # Classes to initialize.
        self.manual_class = manual.Manual  # REQUIRED
        self.auto_class = auto.Auto
        self.ROVInfo = rov_info.ROVInfo

        # Main functions.
        self.manual_intercepts = self.manual_class.manual_intercepts  # REQUIRED
        self.auto_processing = self.auto_class.auto_processing

