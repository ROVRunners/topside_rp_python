import rov_config
from io_systems.io_handler import IO


class GenericROV:

    def __init__(self, config: rov_config.ROVConfig, io: IO) -> None:
        """Create and initialize the ROV hardware.

        Args:
            config (rov_config.ROVConfig):
                ROV hardware configuration.
            io (IO):
                The IO object.
        """
        self._config = config
        self._io = io

    def loop(self) -> None:
        """Run the ROV."""
        pass

    def shutdown(self) -> None:
        """Shutdown the ROV."""
        pass
