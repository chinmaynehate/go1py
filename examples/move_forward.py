import asyncio
import logging
import sys
import time
from go1pylib import Go1, Go1Mode

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more information
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        logger.info("Initializing Go1 robot...")
        dog = Go1()
        
        logger.info("Connecting to robot...")
        dog.init()
        
        # Wait to ensure we're connected
        logger.info("Waiting for connection...")
        start_time = time.time()
        while not dog.mqtt.connected and (time.time() - start_time) < 10:
            await asyncio.sleep(0.1)
        
        if not dog.mqtt.connected:
            logger.error("Failed to connect to robot")
            sys.exit(1)
        
        logger.info("Connected successfully")
        
        # Set to walk mode
        logger.info("Setting walk mode")
        dog.set_mode(Go1Mode.WALK)
        await asyncio.sleep(2)  # Wait longer for mode to take effect
        
        # Move forward
        logger.info("Moving forward...")
        await dog.go_forward(speed=0.25, duration_ms=2000)
        
        logger.info("Movement complete")
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        if 'dog' in locals():
            logger.info("Disconnecting...")
            dog.mqtt.disconnect()

if __name__ == "__main__":
    asyncio.run(main())