import copy
import subprocess
import time
from threading import Lock
from hardware.pin import Pin
from hardware.i2c import I2C
import json
from enums import MavlinkMessageTypes

import killport
import paho.mqtt.client as mqtt_c


class ROVConnection:
    """A class to handle the connection between the Raspberry Pi and the PC.

    Methods:
        connect() -> None:
            Connect to the MQTT broker.
        publish_commands(command_list: dict[str, str | float]) -> None:
            Send a series of packets to the Raspberry Pi with the specified commands.
        publish_i2c(i2cs: dict[str, I2C]) -> None:
            Send a series of packets from the Raspberry Pi with the specified I2C values.
        publish_pins(pins: dict[str, Pin]) -> None:
            Send a series of packets from the Raspberry Pi with the specified thruster PWM values.
        get_subscriptions() -> dict[str, float | str | dict[str, float | str]]:
            Get the sensor data from the Raspberry Pi.
        shutdown() -> None:
            Disconnect from the MQTT broker.
    """

    def __init__(self, ip: str = "localhost", port: int = 1883, client_id: str = "PC") -> None:
        """Initialize the SurfaceConnection object.

        Args:
            ip (str, optional):
                The IP address of the MQTT broker.
                Defaults to "localhost".
            port (int, optional):
                The port of the MQTT broker.
                Defaults to 1883.
            client_id (str, optional):
                The ID of the computer connecting to the MQTT broker.
                Defaults to "PC".
        """
        self._ip = ip
        self._port = port
        self._client_id = client_id

        # TODO: Figure this out: callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        self._client = mqtt_c.Client(client_id=self._client_id)

        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        # self._client.on_publish = self._on_publish
        # self._client.on_subscribe = self._on_subscribe
        # self._client.on_disconnect = self._on_disconnect

        self._subscription_lock: Lock = Lock()
        self._subscriptions = {}

        # Store the last pin configs to only send the ones that have changed.
        self._last_pin_configs: dict[str, Pin] = {}
        self._last_pin_update: float = 0.0
        self._idle_ping_frequency: float = 2.0

        self._last_i2c_configs: dict[str, I2C] = {}
        self._last_i2c_update: float = 0.0

        self._last_mavlink_requests: dict[int, tuple[int, int, int, int, int, int, int]] = {}
        self._last_mavlink_update: float = 0.0

        # Do the same for commands.
        self._last_command_values = {}
        self._last_command_update: float = 0.0

    def connect(self) -> None:
        """Connect to the MQTT broker."""
        try:
            killport.kill_ports(ports=[1883])
        except:
            pass
        # you must have mosquitto installed and the conf file for this to work
        subprocess.Popen(
            '\"C:\\Program Files\\mosquitto\\mosquitto.exe\" -v -c \"C:\\Program Files\\mosquitto\\mosquitto.conf\"',
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        self._client.connect(host=self._ip, port=self._port)
        self._client.loop_start()

        time.sleep(1)

    def publish_commands(self, command_list: dict[str, str | float]) -> None:
        """Send a series of packets to the Raspberry Pi with the specified commands.

        Args:
            command_list (dict[str, str | float]):
                List of commands to be sent to the ROV, such as solenoid toggling, servo moving, or variable modifying.
                Each command key must be specifically subscribed to by the ROV. One such use could be to command the ROV
                to subscribe to a new topic, however. Another note is that the value could be a json string, therefore
                allowing for different types of data to be sent.
        """
        # Build a dictionary of the PWM values that have changed.
        changed_command_values = {}

        for cmd, value in command_list.items():
            if value != self._last_command_values.get(cmd, 0):
                self._last_command_values[cmd] = value
                changed_command_values[cmd] = value

        # If no values have changed for too long, send the last values every 0.5 seconds.
        if not changed_command_values:
            if time.time() - self._last_command_update > self._idle_ping_frequency:
                changed_command_values = copy.deepcopy(self._last_command_values)

        # Update the last PWM update time regardless of whether the PWM values have changed.
        self._last_command_update = time.time()

        for cmd, val in changed_command_values.items():
            self._client.publish(f"PC/commands/{cmd}", val)

    def publish_i2c(self, i2cs: dict[str, I2C]) -> None:
        """Send a series of packets from the Raspberry Pi with the specified I2C values. To improve
        performance, only put the sending_vals that have changed into the dictionary.

        Args:
            i2cs (dict[str, I2C]):
                List of I2C values to be sent to the ROV.
        """
        # Build a dictionary of the PWM values that have changed.
        changed_i2c_configs = {}

        # print(self._last_pin_configs)
        for i2c, config in i2cs.items():
            if i2c in self._last_i2c_configs.keys():
                if config != self._last_i2c_configs.get(i2c, None):
                    changed_i2c_configs[i2c] = copy.deepcopy(config)
                    self._last_i2c_configs[i2c] = copy.deepcopy(config)
            else:
                changed_i2c_configs[i2c] = copy.deepcopy(config)
                self._last_i2c_configs[i2c] = copy.deepcopy(config)

        # If no values have changed for too long, send the last values every 0.5 seconds.
        # if not changed_i2c_configs:
        #     if time.time() - self._last_i2c_update > self._idle_ping_frequency:
        #         changed_i2c_configs = copy.deepcopy(self._last_i2c_configs)
        #         self._last_i2c_update = time.time()
        # else:
        #     # Update the last PWM update time
        #     self._last_i2c_update = time.time()



        # Publish the PWM values to the MQTT broker.
        for pos, value in changed_i2c_configs.items():
            # print("Pin:", value.id, "Value:", value.val)
            self._client.publish(f"PC/i2c/{pos}/addr", value.addr)
            self._client.publish(f"PC/i2c/{pos}/send_vals", json.dumps(value.sending_vals))
            self._client.publish(f"PC/i2c/{pos}/read_regs", json.dumps(value.reading_registers))
            self._client.publish(f"PC/i2c/{pos}/poll_vals", json.dumps(value.poll_val))


    def publish_pins(self, pins: dict[str, Pin]) -> None:
        """Send a series of packets from the Raspberry Pi with the specified thruster PWM values. To improve
        performance, only put the PWM values that have changed into the dictionary.

        Args:
            pins (dict[str, Pin]):
                List of pin values to be sent to the ROV.
        """

        # Build a dictionary of the PWM values that have changed.
        changed_pin_configs = {}

        # print(self._last_pin_configs)
        for pin, config in pins.items():
            if pin in self._last_pin_configs.keys():
                if config != self._last_pin_configs.get(pin, None):
                    changed_pin_configs[pin] = copy.deepcopy(config)
                    self._last_pin_configs[pin] = copy.deepcopy(config)
            else:
                changed_pin_configs[pin] = copy.deepcopy(config)
                self._last_pin_configs[pin] = copy.deepcopy(config)

        # If no values have changed for too long, send the last values every 0.5 seconds.
        if not changed_pin_configs:
            if time.time() - self._last_pin_update > self._idle_ping_frequency:
                changed_pin_configs = copy.deepcopy(self._last_pin_configs)
                self._last_pin_update = time.time()
        # else:
        #     # Update the last PWM update time
        #     self._last_pin_update = time.time()



        # Publish the PWM values to the MQTT broker.
        for pos, value in changed_pin_configs.items():
            # print("Pin:", value.id, "Value:", value.val)
            self._client.publish(f"PC/pins/{pos}/id", value.id)
            self._client.publish(f"PC/pins/{pos}/mode", value.mode)
            self._client.publish(f"PC/pins/{pos}/val", value.val)
            self._client.publish(f"PC/pins/{pos}/freq", value.freq)

    def publish_mavlink_commands(self, commands: dict[int, tuple[int, int, int, int, int, int, int]]) -> None:
        """Send a series of packets from the Raspberry Pi with the specified mavlink commands.

        Args:
            commands (dict[int, tuple[int, int, int, int, int, int, int]]):
                List of mavlink commands to be sent to the ROV.
                dict[message_type, tuple[param1, param2, param3, param4, param5, param6, param7]]
        """

        # changed_mavlink_requests = {}

        # for key, interval in commands.items():
        #     if key not in self._last_mavlink_requests:
        #         self._last_mavlink_requests[key] = interval
        #         changed_mavlink_requests[key] = interval
        #     elif self._last_mavlink_requests[
        #         key] != interval or time.time() - self._last_mavlink_update > self._idle_ping_frequency:
        #         self._last_mavlink_requests[key] = interval
        #         changed_mavlink_requests[key] = interval

        for key, payload in commands.items():
            # self._last_mavlink_update = time.time()
            print(f"Publishing {payload} to {key}")
            self._client.publish(f"PC/mavlink/send_msg/{key}", str(payload)[1:-1])

        commands.clear()

    def publish_mavlink_params(self, params: dict[int, tuple[int, int, int, int, int, int, int]]) -> None:
        """Send a series of packets from the Raspberry Pi with the specified mavlink parameters."""
        for key, payload in params.items():
            # self._last_mavlink_update = time.time()
            print(f"Publishing {payload} to {key}")
            self._client.publish(f"PC/mavlink/send_msg/{key}", str(payload)[1:-1])

        params.clear()

    def publish_mavlink_data_request(self, mavlink: dict[int, int]) -> None:
        """Send a series of packets from the Raspberry Pi with the specified mavlink data id and interval values.

        Args:
            mavlink (dict[int, int]):
                List of mavlink values to be sent to the ROV.
        """
        # changed_mavlink_requests = {}

        # for key, interval in mavlink.items():
        #     if key not in self._last_mavlink_requests:
        #         self._last_mavlink_requests[key] = interval
        #         changed_mavlink_requests[key] = interval
        #     elif self._last_mavlink_requests[key] != interval or time.time() - self._last_mavlink_update > self._idle_ping_frequency:
        #         self._last_mavlink_requests[key] = interval
        #         changed_mavlink_requests[key] = interval

        

        changed_mavlink_requests = {}

        for key, interval in mavlink.items():
            if key not in self._last_mavlink_requests:
                self._last_mavlink_requests[key] = interval
                changed_mavlink_requests[key] = interval
            elif self._last_mavlink_requests[
                key] != interval or time.time() - self._last_mavlink_update > self._idle_ping_frequency:
                self._last_mavlink_requests[key] = interval
                changed_mavlink_requests[key] = interval

        for key, interval in changed_mavlink_requests.items():
            self._last_mavlink_update = time.time()
            self._client.publish(f"PC/mavlink/req_id/{key}", interval)

    def get_subscriptions(self) -> dict[str, float | str | dict[str, float | str]]:
        """Get the sensor data from the Raspberry Pi.

        Returns:
            dict[str, float | str | dict[str, float | str]]: A dictionary of the sensor data with the key as the sensor
                name, the status of the ROV, and other misc. data.
        """
        # Make a copy of the subscriptions to get the values out as fast as possible.
        original_vals = {}
        with self._subscription_lock:
            original_vals |= copy.deepcopy(self._subscriptions)

        # Decode the JSON strings and return the dictionary.
        decoded_vals = {}
        for key, val in original_vals.items():
            try:
                decoded_vals[key] = json.loads(val)
            except json.JSONDecodeError:
                decoded_vals[key] = val

        return decoded_vals

    def _set_subscription_value(self, sub: str, value: str | float) -> None:
        """Set the subscription dictionary values.

        Args:
            sub (str):
                The subscription to set the value for.
            value (str | float):
                The value to set the subscription to.
        """
        with self._subscription_lock:
            self._subscriptions[sub] = value

    def _on_message(self, client, userdata, message) -> None:
        """Handle incoming messages from the MQTT broker.

        Args:
            client (mqtt.Client):
                The client object.
            userdata:
                The user data.
            message (mqtt.MQTTMessage):
                The message object.
        """
        # print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

        self._set_subscription_value(message.topic, message.payload.decode())

    def _on_connect(self, client, userdata, flags, rc) -> None:
        """Handle connection to the MQTT broker.

        Args:
            client (mqtt.Client):
                The client object.
            userdata:
                The user data.
            flags:
                The flags.
            rc (int):
                The result code.
        """
        print(f"Connected with result code {rc}")

        self._client.subscribe("ROV/#")

    # def _on_publish(self, client, userdata, mid):
    #     print(f"Published message with mid {mid}")
    #
    # def _on_subscribe(self, client, userdata, mid, granted_qos):
    #     print(f"Subscribed to topic with mid {mid} and QoS {granted_qos}")
    #
    # def _on_disconnect(self, client, userdata, rc):
    #     print(f"Disconnected with result code {rc}")

    def shutdown(self):
        self._client.loop_stop()
        self._client.disconnect()
        print("Disconnected from MQTT broker.")


if __name__ == "__main__":
    connection = ROVConnection()
    connection.connect()
