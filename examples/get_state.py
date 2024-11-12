import asyncio
import logging
from typing import Optional
from go1py.go1 import Go1, Go1Mode
from go1py.mqtt.state import Go1State

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BatteryMonitor:
    """Monitor and handle battery state changes."""
    
    def __init__(self, dog: Go1):
        """
        Initialize the battery monitor.
        
        Args:
            dog: Initialized Go1 instance
        """
        self.dog = dog

    def handle_battery(self, state: Go1State) -> None:
        """
        Handle battery state changes and set LED color accordingly.
        
        Args:
            state: Current state of the Go1 robot
            
        LED Colors:
        - Green (>= 75%)
        - Orange (50-74%)
        - Red (< 25%)
        """
        battery_level = state.bms.soc
        logger.info(f"Battery level: {battery_level}%")
        
        if battery_level >= 75:
            self.dog.set_led_color(0, 255, 0)  # Green
        elif 50 <= battery_level < 75:
            self.dog.set_led_color(255, 127, 0)  # Orange
        elif battery_level < 25:
            self.dog.set_led_color(255, 0, 0)  # Red

async def demo_movement(dog: Go1) -> None:
    """
    Demonstrate simple movement pattern.
    
    Args:
        dog: Initialized Go1 instance
    """
    try:
        while True:
            logger.info("Setting mode to STAND_DOWN")
            dog.set_mode(Go1Mode.STAND_DOWN)
            await asyncio.sleep(2)
            
            logger.info("Setting mode to STAND_UP")
            dog.set_mode(Go1Mode.STAND)
            await asyncio.sleep(2)
            
            logger.info("Moving forward")
            await dog.go_forward(speed=0.2, duration_ms=1000)
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        logger.info("Movement demo cancelled")
    except Exception as e:
        logger.error(f"Error during movement: {str(e)}")

async def main():
    """
    Main function demonstrating state monitoring and LED feedback.
    
    This example:
    1. Sets up battery state monitoring
    2. Changes LED color based on battery level
    3. Demonstrates simple movement pattern
    """
    # Initialize robot
    logger.info("Initializing Go1 robot...")
    dog = Go1()
    dog.init()
    
    # Wait for connection
    timeout = 10
    start_time = time.time()
    while not dog.mqtt.connected and (time.time() - start_time < timeout):
        await asyncio.sleep(0.1)
        
    if not dog.mqtt.connected:
        logger.error("Failed to connect to robot")
        return
    
    # Set up battery monitor
    monitor = BatteryMonitor(dog)
    
    # Set up state change handler
    def on_state_change(state: Go1State):
        monitor.handle_battery(state)
    
    dog.on('go1_state_change', on_state_change)
    
    try:
        # Run movement demo
        await demo_movement(dog)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
    finally:
        # Clean up
        if dog.mqtt.connected:
            dog.set_led_color(0, 0, 0)  # Turn off LED
            dog.mqtt.disconnect()
        logger.info("Disconnected from robot.")

if __name__ == "__main__":
    asyncio.run(main())
