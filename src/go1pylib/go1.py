from enum import Enum
from typing import Optional, Dict, Any
import asyncio
from dataclasses import dataclass
from events import Events

class Go1Mode(str, Enum):
    """Available modes for the Go1 robot."""
    DANCE1 = "dance1"
    DANCE2 = "dance2"
    STRAIGHT_HAND1 = "straightHand1"
    DAMPING = "damping"
    STAND_UP = "standUp"
    STAND_DOWN = "standDown"
    RECOVER_STAND = "recoverStand"
    STAND = "stand"
    WALK = "walk"
    RUN = "run"
    CLIMB = "climb"

class Go1(Events):
    """
    Main class for controlling the Go1 quadruped robot.
    
    This class provides high-level control interfaces for the Go1 robot,
    including movement, pose control, LED control, and mode settings.
    """

    def __init__(self, mqtt_options: Optional[Dict[str, Any]] = None):
        """
        Initialize a new Go1 robot controller.

        Args:
            mqtt_options: Optional MQTT client configuration options
        """
        super().__init__()
        # These will be imported from their respective modules once we convert them
        from .mqtt.client import Go1MQTT
        from .mqtt.state import Go1State, get_go1_state_copy
        
        self.mqtt = Go1MQTT(self, mqtt_options)
        self.go1_state = get_go1_state_copy()

    def init(self) -> None:
        """Initialize the connection to the robot."""
        self.mqtt.connect()
        self.mqtt.subscribe()

    def publish_state(self, state: 'Go1State') -> None:
        """
        Publish a new robot state.

        Args:
            state: Current state of the Go1 robot
        """
        self.emit('go1_state_change', state)

    def publish_connection_status(self, connected: bool) -> None:
        """
        Publish the connection status.

        Args:
            connected: Whether the robot is connected
        """
        self.emit('go1_connection_status', connected)

    async def go_forward(self, speed: float, duration_ms: int) -> None:
        """
        Move forward based on speed and time.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, 0, 0, speed)
        await self.mqtt.send_movement_command(duration_ms)

    async def go_backward(self, speed: float, duration_ms: int) -> None:
        """
        Move backward based on speed and time.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, 0, 0, -speed)
        await self.mqtt.send_movement_command(duration_ms)

    async def go_left(self, speed: float, duration_ms: int) -> None:
        """
        Move left based on speed and time.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(-speed, 0, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def go_right(self, speed: float, duration_ms: int) -> None:
        """
        Move right based on speed and time.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(speed, 0, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def go(self, left_right_speed: float, turn_speed: float, 
                 forward_speed: float, duration_ms: int) -> None:
        """
        Combined movement in multiple directions.

        Args:
            left_right_speed: A value from -1 to 1
            turn_speed: A value from -1 to 1
            forward_speed: A value from -1 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(left_right_speed, turn_speed, 0, forward_speed)
        await self.mqtt.send_movement_command(duration_ms)

    async def turn_left(self, speed: float, duration_ms: int) -> None:
        """
        Rotate left based on speed and time.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, -speed, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def turn_right(self, speed: float, duration_ms: int) -> None:
        """
        Rotate right based on speed and time.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, speed, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def pose(self, lean: float, twist: float, look: float, 
                  extend: float, duration_ms: int) -> None:
        """
        Raw pose method for accessing all axes together. Requires stand mode.

        Args:
            lean: Lean left/right amount (-1 to 1)
            twist: Twist left/right amount (-1 to 1)
            look: Look up/down amount (-1 to 1)
            extend: Extend/squat amount (-1 to 1)
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(lean, twist, look, extend)
        await self.mqtt.send_movement_command(duration_ms)

    async def extend_up(self, speed: float, duration_ms: int) -> None:
        """
        Extend up - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, 0, 0, speed)
        await self.mqtt.send_movement_command(duration_ms)

    async def squat_down(self, speed: float, duration_ms: int) -> None:
        """
        Squat down - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, 0, 0, -speed)
        await self.mqtt.send_movement_command(duration_ms)

    async def lean_left(self, speed: float, duration_ms: int) -> None:
        """
        Lean body to the left - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(-speed, 0, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def lean_right(self, speed: float, duration_ms: int) -> None:
        """
        Lean body to the right - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(speed, 0, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def twist_left(self, speed: float, duration_ms: int) -> None:
        """
        Twist body to the left - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, -speed, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def twist_right(self, speed: float, duration_ms: int) -> None:
        """
        Twist body to the right - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, speed, 0, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def look_down(self, speed: float, duration_ms: int) -> None:
        """
        Look down - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, 0, speed, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def look_up(self, speed: float, duration_ms: int) -> None:
        """
        Look up - requires stand mode.

        Args:
            speed: A value from 0 to 1
            duration_ms: Length of time for movement in milliseconds
        """
        self.mqtt.update_speed(0, 0, -speed, 0)
        await self.mqtt.send_movement_command(duration_ms)

    async def reset_body(self) -> None:
        """Helper function to clear out previous queued movements."""
        self.mqtt.update_speed(0, 0, 0, 0)
        await self.mqtt.send_movement_command(1000)

    async def wait(self, duration_ms: int) -> None:
        """
        Wait for a period of time.

        Args:
            duration_ms: Length of time to wait in milliseconds
        """
        await asyncio.sleep(duration_ms / 1000.0)

    def set_led_color(self, r: int, g: int, b: int) -> None:
        """
        Change Go1's LED color.

        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        """
        self.mqtt.send_led_command(r, g, b)

    def set_mode(self, mode: Go1Mode) -> None:
        """
        Set Go1's operation mode.

        Args:
            mode: The mode to set the robot to
        """
        self.mqtt.send_mode_command(mode)