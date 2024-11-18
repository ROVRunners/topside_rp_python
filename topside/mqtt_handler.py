import copy
import json
import time
from threading import Lock

import paho.mqtt.client as mqtt

from rovs.spike import enums


class ROVConnection:
    def __init__(self, ip: str = "localhost", port: int = 1883, client_id: str = "ROV_Controller") -> None:
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
                Defaults to "ROV_Controller".
        """
        self._ip = ip
        self._port = port
        self._client_id = client_id

        self._client = mqtt.Client(client_id=self._client_id)

        self._client.on_message = self._on_message
        self._client.on_connect = self._on_connect
        # self._client.on_publish = self._on_publish
        # self._client.on_subscribe = self._on_subscribe
        # self._client.on_disconnect = self._on_disconnect

        self._subscription_lock: Lock = Lock()
        self._subscriptions = {}

        # Store the last PWM values to only send the ones that have changed.
        self._last_pwm_values = {}
        self._last_pwm_update: float = 0.0
        self._idle_ping_frequency: float = 0.5

    def connect(self):
        self._client.connect(host=self._ip, port=self._port)
        self._client.loop_start()

    def publish_commands(self, command_list: dict[str, str | float]) -> None:
        """Send a series of packets to the Raspberry Pi with the specified commands.

        Args:
            command_list (dict[str, str | float]):
                List of commands to be sent to the ROV, such as solenoid toggling, servo moving, or variable modifying.
                Each command key must be specifically subscribed to by the ROV. One such use could be to command the ROV
                to subscribe to a new topic, however. Another note is that the value could be a json string, therefore
                allowing for different types of data to be sent.
                TODO: Implement these in the ROV.
        """
        for cmd, val in command_list.items():
            self._client.publish(cmd, val)

    def publish_thruster_pwm(self, thruster_pwm: dict[enums.ThrusterPositions, int]) -> None:
        """Send a series of packets from the Raspberry Pi with the specified thruster PWM values. To improve
        performance, only put the PWM values that have changed into the dictionary.

        Args:
            thruster_pwm (dict[enums.ThrusterPositions, int]):
                The thruster PWM values to send to the surface.
        """
        # Build a dictionary of the PWM values that have changed.
        changed_pwm_values = {}

        for thruster, pwm in thruster_pwm.items():
            if pwm != self._last_pwm_values.get(thruster, 0):
                self._last_pwm_values[thruster] = pwm
                changed_pwm_values[thruster] = pwm

        # If no values have changed for too long, send the last values every 0.5 seconds.
        if not changed_pwm_values:
            if time.time() - self._last_pwm_update > self._idle_ping_frequency:
                changed_pwm_values = copy.deepcopy(self._last_pwm_values)
            else:
                return

        # Update the last PWM update time regardless of whether the PWM values have changed.
        self._last_pwm_update = time.time()

        # Publish the PWM values to the MQTT broker.
        for pos, value in changed_pwm_values.items():
            self._client.publish(f"thruster_pwm/{pos}", value)

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

    def _on_message(self, client, userdata, message):
        print(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

        self._set_subscription_value(message.topic, message.payload.decode())

    def _on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

        self._client.subscribe("ROV_sensor_data")
        self._client.subscribe("ROV_status")
        self._client.subscribe("ROV_other")

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
