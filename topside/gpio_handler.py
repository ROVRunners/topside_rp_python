from pin import Pin
import enums


class GPIOHandler:
    def __init__(self, pins: dict[str, Pin]) -> None:
        """Initialize the SurfaceConnection object.

        Args: pins (dict[str, PinConfig])

        """

        self._pins = pins

    def update_motor_pwm(self, thruster_pwm: dict[enums.ThrusterPositions, int]) -> None:
        """"""
        for thruster, val in thruster_pwm.items():
            self.pins[thruster].val = val

    #TODO add the pin if it does not exist
    def update(self, subs: dict[str, str]) -> None:
        for i in subs.keys():
            if i.startswith("ROV/pins/"):
                self.pins[i.split("/")[2]].val = int(subs[i])

    @property
    def pins(self) -> dict[str, Pin]:
        return self._pins

    @pins.setter
    def pins(self, pins: dict[str, Pin]) -> None:
        self._pins = pins



