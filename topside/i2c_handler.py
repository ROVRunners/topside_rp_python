from i2c import I2C
import enums


class I2CHandler:
    def __init__(self, i2cs: dict[str, I2C]) -> None:
        """Initialize the SurfaceConnection object.

        Args: i2cs (dict[str, I2CConfig])

        """

        self._i2cs = i2cs

    # TODO add the i2c if it does not exist
    def update(self, subs: dict[str, str]) -> None:
        for i in subs.keys():
            if i.startswith("ROV/i2c/"):
                self._i2cs[i.split("/")[2]].received_vals[i.split("/")[3]] = int(subs[i])


    @property
    def i2cs(self) -> dict[str, I2C]:
        return self._i2cs

    @i2cs.setter
    def i2cs(self, i2cs: dict[str, I2C]) -> None:
        self._i2cs = i2cs



