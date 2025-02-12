from typing import Callable

from dashboard import Dashboard
from hardware.thruster_pwm import FrameThrusters
from io_systems.io_handler import IO
from kinematics import Kinematics


class ControlMode:
    """The ControlMode class is the base class for all control modes.

    Methods:
        update() -> None:
            Update the control mode.
        shutdown() -> None:
            Shutdown the control mode.
    """

    def __init__(self, frame: FrameThrusters, io: IO, kinematics: Kinematics, set_control_mode: Callable,
                 dash: Dashboard) -> None:
        """Initialize the Manual object.

        Args:
            frame (FrameThrusters):
                The objects of the thrusters mounted to the frame.
            io (IO):
                The IO (input output) object.
            kinematics (Kinematics):
                The Kinematics object housing the PIDs.
            set_control_mode (Callable):
                The function to set the control mode.
            dash (Dashboard):
                The Tkinter Dashboard object.
        """
        self._frame = frame
        self._io = io
        self._kinematics = kinematics
        self._set_control_mode = set_control_mode
        self._dash = dash

    def loop(self) -> None:
        """Update the control mode."""
        raise NotImplementedError

    def shutdown(self) -> None:
        """Shutdown the control mode."""
        raise NotImplementedError
