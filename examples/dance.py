import asyncio
import logging
import time
from go1pylib.go1 import Go1, Go1Mode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def perform_dance_sequence(dog: Go1, intensity: float = 0.5) -> None:
    """
    Perform a sequence of dance movements.
    
    Args:
        dog: Initialized Go1 instance
        intensity: Movement intensity/speed (0.0 to 1.0)
    """
    # Sequence of movements with consistent timing
    movements = [
        (dog.look_up, "Looking up"),
        (dog.look_down, "Looking down"),
        (dog.lean_left, "Leaning left"),
        (dog.lean_right, "Leaning right"),
        (dog.twist_left, "Twisting left"),
        (dog.twist_right, "Twisting right")
    ]
    
    for movement, description in movements:
        if not dog.mqtt.connected:
            logger.error("Lost connection during dance")
            return
            
        logger.info(description)
        await movement(speed=intensity, duration_ms=1000)
        await asyncio.sleep(0.5)  # Small pause between movements

async def main():
    """
    Main function executing a dance routine with the Go1 robot.
    """
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
            
        # Initial wait for robot to stabilize
        logger.info("Waiting for robot to stabilize")
        await asyncio.sleep(3)
        
        # Set to stand mode for dance
        logger.info("Setting stand mode")
        dog.set_mode(Go1Mode.STAND)
        await asyncio.sleep(2)  # Wait longer for mode to take effect
        
        try:
            # First sequence - 50% intensity
            logger.info("Starting dance sequence at 50% intensity")
            await perform_dance_sequence(dog, intensity=0.5)
            await dog.reset_body()
            await asyncio.sleep(1)
            
            # Second sequence - 100% intensity
            logger.info("Starting dance sequence at 100% intensity")
            await perform_dance_sequence(dog, intensity=1.0)
            await dog.reset_body()
            await asyncio.sleep(1)
            
            # Return to walk mode
            logger.info("Returning to walk mode")
            dog.set_mode(Go1Mode.WALK)
            
            logger.info("Dance routine completed successfully")
            
        except Exception as e:
            logger.error(f"Error during dance sequence: {str(e)}")
        finally:
            # Always ensure we reset the body
            await dog.reset_body()
            
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