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

async def move_in_square(dog: Go1, side_length: float = 2.0, speed: float = 0.3) -> None:
    """
    Move the robot in a square pattern.
    
    Args:
        dog: Initialized Go1 instance
        side_length: Length of each side in seconds
        speed: Movement speed (0.0 to 1.0)
    """
    # Define square movements
    movements = [
        (dog.go_forward, "Moving forward"),
        (dog.turn_right, "Turning right"),
        (dog.go_forward, "Moving forward"),
        (dog.turn_right, "Turning right"),
        (dog.go_forward, "Moving forward"),
        (dog.turn_right, "Turning right"),
        (dog.go_forward, "Moving forward"),
        (dog.turn_right, "Turning right"),
    ]
    
    turn_duration = 1500  # 1.5 seconds for 90-degree turn
    move_duration = int(side_length * 1000)  # Convert seconds to milliseconds
    
    for i, (movement, description) in enumerate(movements):
        if not dog.mqtt.connected:
            logger.error("Lost connection to robot")
            return
            
        logger.info(f"Step {i+1}/8: {description}")
        
        # Use different duration and speed for turns vs straight movements
        if "Turning" in description:
            await movement(speed=speed, duration_ms=turn_duration)
        else:
            await movement(speed=speed, duration_ms=move_duration)
        
        # Small pause between movements
        await asyncio.sleep(0.5)

async def main():
    """
    Main function demonstrating square movement pattern.
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
        
        # Set walk mode
        logger.info("Setting walk mode")
        dog.set_mode(Go1Mode.WALK)
        await asyncio.sleep(2)  # Wait for mode to take effect
        
        try:
            # Execute square movement pattern
            logger.info("Starting square movement pattern")
            await move_in_square(dog, side_length=2.0, speed=0.3)
            logger.info("Square movement completed successfully")
            
        except Exception as e:
            logger.error(f"Error during movement: {str(e)}")
        finally:
            # Return to standing position
            logger.info("Returning to stand down position")
            dog.set_mode(Go1Mode.STAND_DOWN)
            await asyncio.sleep(1)
            
    except Exception as e:
        logger.error(f"Error initializing robot: {str(e)}")
    finally:
        if 'dog' in locals():
            logger.info("Disconnecting...")
            dog.mqtt.disconnect()

def print_menu():
    """Print the available options menu."""
    print("\nGo1 Square Movement Options:")
    print("1. Small square (2 seconds per side)")
    print("2. Medium square (3 seconds per side)")
    print("3. Large square (4 seconds per side)")
    print("4. Custom square")
    print("0. Exit")

async def interactive_main():
    """Interactive main function allowing user to choose square size."""
    try:
        # Initialize robot
        logger.info("Initializing Go1")
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

        while True:
            print_menu()
            choice = input("Select an option (0-4): ")

            if choice == "0":
                break
            elif choice == "1":
                side_length = 2.0
                speed = 0.3
            elif choice == "2":
                side_length = 3.0
                speed = 0.3
            elif choice == "3":
                side_length = 4.0
                speed = 0.3
            elif choice == "4":
                side_length = float(input("Enter side length in seconds (1-5): "))
                speed = float(input("Enter speed (0.1-0.5): "))
                side_length = max(1.0, min(5.0, side_length))
                speed = max(0.1, min(0.5, speed))
            else:
                print("Invalid choice!")
                continue

            try:
                # Set walk mode
                logger.info("Setting walk mode")
                dog.set_mode(Go1Mode.WALK)
                await asyncio.sleep(2)
                
                # Execute movement
                await move_in_square(dog, side_length, speed)
                
                # Return to stand
                dog.set_mode(Go1Mode.STAND_DOWN)
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error during movement: {e}")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if 'dog' in locals():
            logger.info("Disconnecting...")
            dog.mqtt.disconnect()

if __name__ == "__main__":
    try:
        # Use interactive_main() for user input, or main() for single run
        asyncio.run(interactive_main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
