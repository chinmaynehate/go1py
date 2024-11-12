import asyncio
import logging
import time
from typing import Optional
from go1py.go1 import Go1, Go1Mode
from go1py.mqtt.state import Go1State

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CollisionAvoidance:
    """Handles collision avoidance behavior for Go1."""
    
    def __init__(self, dog: Go1, warning_threshold: float = 0.75):
        self.dog = dog
        self.warning_threshold = warning_threshold
        self.stop_requested = False
        self.last_warning_time = 0
        # Movement states
        self.current_speed = 0.3  # Default forward speed
        self.is_moving = False
        self.is_turning = False
        self.turn_direction = "right"  # Default turn direction

    async def start_moving(self):
        """Start moving forward."""
        logger.info("Moving forward")
        self.is_moving = True
        await self.dog.go_forward(self.current_speed, 1000)

    async def stop_moving(self):
        """Stop all movement."""
        logger.info("Stopping")
        self.is_moving = False
        await self.dog.go_forward(0, 500)

    async def turn(self, direction: str):
        """
        Turn in the specified direction.
        
        Args:
            direction: "left" or "right"
        """
        logger.info(f"Turning {direction}")
        self.is_turning = True
        turn_speed = 0.5
        
        if direction == "left":
            await self.dog.turn_left(turn_speed, 1000)
        else:
            await self.dog.turn_right(turn_speed, 1000)
        await asyncio.sleep(1)  # Brief pause to complete turn

    def handle_collision_detection(self, state: Go1State) -> None:
        """Process distance warnings and respond to potential collisions."""
        current_time = time.time()
        if current_time - self.last_warning_time < 0.1:  # Limit warning rate
            return

        # Get distance warnings from all directions
        warnings = state.robot.distance_warning
        front_warning = warnings.front
        left_warning = warnings.left
        right_warning = warnings.right
        
        logger.debug(f"Warnings - Front:{front_warning:.2f}, Left:{left_warning:.2f}, Right:{right_warning:.2f}")

        # Collision detection logic with LED feedback
        if front_warning < self.warning_threshold:
            self.stop_requested = True
            self.turn_direction = "right" if left_warning < right_warning else "left"
            self.dog.set_led_color(255, 0, 0)  # Red
        elif left_warning < self.warning_threshold:
            self.stop_requested = True
            self.turn_direction = "right"
            self.dog.set_led_color(255, 165, 0)  # Orange
        elif right_warning < self.warning_threshold:
            self.stop_requested = True
            self.turn_direction = "left"
            self.dog.set_led_color(255, 165, 0)  # Orange
        else:
            self.stop_requested = False
            self.dog.set_led_color(0, 255, 0)  # Green

        self.last_warning_time = current_time

async def avoidance_behavior(avoider: CollisionAvoidance) -> None:
    """Main avoidance behavior loop."""
    while True:
        try:
            if not avoider.dog.mqtt.connected:
                logger.error("Lost connection to robot")
                break
            
            if avoider.stop_requested:
                await avoider.stop_moving()
                await avoider.turn(avoider.turn_direction)
                await asyncio.sleep(1)  # Wait before checking surroundings again
            elif not avoider.is_moving:
                await avoider.start_moving()

            await asyncio.sleep(0.1)  # Small delay between checks
            
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Error in avoidance behavior: {e}")
            await avoider.stop_moving()
            break

async def main():
    """Main function demonstrating obstacle avoidance."""
    try:
        # Initialize robot
        logger.info("Initializing Go1")
        dog = Go1()
        
        # Connect to robot
        logger.info("Connecting to robot...")
        dog.init()
        
        # Wait for connection
        timeout = 10
        start_time = time.time()
        while not dog.mqtt.connected and (time.time() - start_time < timeout):
            await asyncio.sleep(0.1)
            
        if not dog.mqtt.connected:
            logger.error("Failed to connect to robot")
            return
        
        # Set up avoidance controller
        avoider = CollisionAvoidance(dog)
        
        # Set up state change handler
        dog.on('go1_state_change', avoider.handle_collision_detection)
        
        try:
            # Set initial mode and LED
            logger.info("Setting walk mode")
            dog.set_mode(Go1Mode.WALK)
            dog.set_led_color(0, 255, 0)  # Green = ready
            await asyncio.sleep(2)  # Wait for mode to take effect
            
            # Start avoidance behavior
            logger.info("Starting obstacle avoidance")
            await avoidance_behavior(avoider)
            
        except KeyboardInterrupt:
            logger.info("Program interrupted by user")
        except Exception as e:
            logger.error(f"Error during operation: {str(e)}")
        finally:
            # Ensure robot is in safe state
            await avoider.stop_moving()
            dog.set_mode(Go1Mode.STAND_DOWN)
            dog.set_led_color(0, 0, 0)  # Turn off LED
            
    except Exception as e:
        logger.error(f"Error initializing robot: {str(e)}")
    finally:
        if 'dog' in locals():
            logger.info("Disconnecting...")
            dog.mqtt.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
