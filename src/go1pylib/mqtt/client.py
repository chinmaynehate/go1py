from typing import Optional, Dict, Any, List
import numpy as np
import paho.mqtt.client as mqtt
import asyncio
from dataclasses import dataclass
import logging
import time

from .state import Go1State, get_go1_state_copy
from .handler import message_handler
from ..go1 import Go1Mode

logger = logging.getLogger(__name__)

@dataclass
class MQTTConfig:
    """Default MQTT configuration for Go1 robot."""
    port: int = 1883
    host: str = "192.168.12.1"
    client_id: str = ""  # Will be randomly generated
    keepalive: int = 60  # Increased from 5 to 60
    protocol: int = mqtt.MQTTv311  # Use v3.1.1 by default

class Go1MQTT:
    """MQTT client for communicating with the Go1 robot."""
    
    def __init__(self, go1: 'Go1', mqtt_options: Optional[Dict[str, Any]] = None):
        """
        Initialize the MQTT client for Go1.
        
        Args:
            go1: Reference to the main Go1 controller
            mqtt_options: Optional MQTT configuration options
        """
        self.go1 = go1
        
        # Set up MQTT configuration
        default_config = MQTTConfig()
        if default_config.client_id == "":
            import random
            import string
            default_config.client_id = ''.join(random.choices(string.hexdigits, k=6))
            
        self.config = default_config
        if mqtt_options:
            for key, value in mqtt_options.items():
                setattr(self.config, key, value)
        
        # Initialize client
        self.client: Optional[mqtt.Client] = None
        self.floats = np.zeros(4, dtype=np.float32)
        self.connected = False
        
        # Topics
        self.movement_topic = "controller/stick"
        self.led_topic = "programming/code"
        self.mode_topic = "controller/action"
        self.publish_frequency = 0.1  # 100ms in seconds
        
        # State
        self.go1_state = get_go1_state_copy()

    def connect(self) -> None:
        """Establish connection to the MQTT broker."""
        logger.info("Connecting to MQTT broker...")
        
        try:
            # Create client with basic options that work across versions
            self.client = mqtt.Client(
                client_id=self.config.client_id,
                clean_session=True,
                protocol=self.config.protocol
            )
            
            # Set up callbacks
            self.client.on_connect = self._on_connect
            self.client.on_disconnect = self._on_disconnect
            self.client.on_message = self._on_message
            self.client.on_publish = self._on_publish
            self.client.on_log = self._on_log
            
            # Connect to broker
            self.client.connect(
                host=self.config.host,
                port=self.config.port,
                keepalive=self.config.keepalive
            )
            self.client.loop_start()
            
            # Wait for connection to establish
            timeout = 10  # seconds
            start_time = time.time()
            while not self.connected:
                if time.time() - start_time > timeout:
                    raise ConnectionError("Connection timeout")
                time.sleep(0.1)
            
            logger.info("Successfully connected to MQTT broker")
            
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise

    def _on_connect(self, client, userdata, flags, rc):
        """Callback for when the client connects to the broker."""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            self.connected = True
            self.go1.publish_connection_status(True)
        else:
            error_messages = {
                1: "Connection refused - incorrect protocol version",
                2: "Connection refused - invalid client identifier",
                3: "Connection refused - server unavailable",
                4: "Connection refused - bad username or password",
                5: "Connection refused - not authorised"
            }
            error_msg = error_messages.get(rc, f"Unknown error code: {rc}")
            logger.error(f"Failed to connect to MQTT broker: {error_msg}")
            self.connected = False

    def _on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker."""
        if rc == 0:
            logger.info("Cleanly disconnected from MQTT broker")
        else:
            logger.warning(f"Unexpectedly disconnected from MQTT broker with code: {rc}")
        self.connected = False
        self.go1.publish_connection_status(False)

    def _on_message(self, client, userdata, msg):
        """Callback for when a message is received."""
        try:
            logger.debug(f"Received message on topic {msg.topic}")
            self.go1.publish_state(self.go1_state)
            message_handler(msg.topic, msg.payload, self.go1_state)
        except Exception as e:
            logger.error(f"Error processing message: {e}")

    def _on_publish(self, client, userdata, mid):
        """Callback for when a message is published."""
        logger.debug(f"Published message {mid}")

    def _on_log(self, client, userdata, level, buf):
        """Callback for logging."""
        logger.debug(f"MQTT Log: {buf}")

    def subscribe(self) -> None:
        """Subscribe to relevant topics."""
        if not self.client:
            logger.error("Cannot subscribe: Client not initialized")
            return
        if not self.connected:
            logger.error("Cannot subscribe: Client not connected")
            return

        try:
            topics = [
                ("bms/state", 0),
                ("firmware/version", 0)
            ]
            self.client.subscribe(topics)
            logger.info(f"Subscribed to topics: {[t[0] for t in topics]}")
        except Exception as e:
            logger.error(f"Error subscribing to topics: {e}")

    def get_state(self) -> Go1State:
        """Get current robot state."""
        return self.go1_state

    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        if self.client:
            try:
                self.client.loop_stop()
                self.client.disconnect()
                logger.info("Disconnected from MQTT broker")
            except Exception as e:
                logger.error(f"Error disconnecting: {e}")

    def update_speed(self, left_right: float, turn_left_right: float,
                    look_up_down: float, backward_forward: float) -> None:
        """
        Update movement speed values.
        
        Args:
            left_right: Left/right movement (-1 to 1)
            turn_left_right: Turn left/right (-1 to 1)
            look_up_down: Look up/down (-1 to 1, stand mode only)
            backward_forward: Forward/backward movement (-1 to 1)
        """
        self.floats[0] = self._clamp(left_right)
        self.floats[1] = self._clamp(turn_left_right)
        self.floats[2] = self._clamp(look_up_down)
        self.floats[3] = self._clamp(backward_forward)
        logger.debug(f"Speed updated: {self.floats}")

    async def send_movement_command(self, duration_ms: int) -> None:
        """
        Send movement command for specified duration.
        
        Args:
            duration_ms: Duration of movement in milliseconds
        """
        if not self.client or not self.connected:
            logger.error("MQTT client not connected")
            return

        try:
            # Send initial zero command
            zero_floats = np.zeros(4, dtype=np.float32)
            info = self.client.publish(
                self.movement_topic,
                zero_floats.tobytes(),
                qos=0
            )
            info.wait_for_publish()  # Wait for the publish to complete
            logger.debug("Sent initial zero command")

            end_time = asyncio.get_event_loop().time() + (duration_ms / 1000.0)
            
            while asyncio.get_event_loop().time() < end_time:
                if not self.connected:
                    logger.error("Lost connection during movement")
                    return
                    
                logger.debug(f"Sending command {self.floats}")
                info = self.client.publish(
                    self.movement_topic,
                    self.floats.tobytes(),
                    qos=0
                )
                info.wait_for_publish()
                await asyncio.sleep(self.publish_frequency)

        except Exception as e:
            logger.error(f"Error sending movement command: {e}")

    def send_led_command(self, r: int, g: int, b: int) -> None:
        """
        Send LED color command.
        
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        """
        if not self.client or not self.connected:
            logger.error("MQTT client not connected")
            return

        try:
            command = f"child_conn.send('change_light({r},{g},{b})')"
            info = self.client.publish(self.led_topic, command, qos=0)
            info.wait_for_publish()
            logger.debug(f"Sent LED command: R={r}, G={g}, B={b}")
        except Exception as e:
            logger.error(f"Error sending LED command: {e}")

    def send_mode_command(self, mode: Go1Mode) -> None:
        """
        Send mode change command.
        
        Args:
            mode: Target mode to set
        """
        if not self.client or not self.connected:
            logger.error("MQTT client not connected")
            return

        try:
            info = self.client.publish(self.mode_topic, mode.value, qos=1)
            info.wait_for_publish()
            logger.info(f"Mode command sent: {mode.value}")
        except Exception as e:
            logger.error(f"Error sending mode command: {e}")

    @staticmethod
    def _clamp(speed: float) -> float:
        """Clamp speed value between -1 and 1."""
        return max(-1.0, min(1.0, speed))
