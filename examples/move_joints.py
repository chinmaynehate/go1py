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

async def demonstrate_direct_poses(dog: Go1):
    """Demonstrate direct pose methods."""
    logger.info("Starting direct pose demonstration")
    
    for _ in range(2):
        logger.info("Extending up")
        await dog.extend_up(speed=1.0, duration_ms=2000)
        await asyncio.sleep(1)  # Pause between movements
        
        logger.info("Squatting down")
        await dog.squat_down(speed=1.0, duration_ms=2000)
        await asyncio.sleep(1)  # Pause between movements

async def demonstrate_generic_poses(dog: Go1):
    """Demonstrate various poses using generic pose method."""
    
    # Leaning poses
    logger.info("Demonstrating lean poses")
    logger.info("Leaning left")
    await dog.pose(lean=-1, twist=0, look=0, extend=0, duration_ms=2000)
    await asyncio.sleep(1)
    
    logger.info("Leaning right")
    await dog.pose(lean=1, twist=0, look=0, extend=0, duration_ms=2000)
    await asyncio.sleep(1)
    
    await dog.reset_body()
    await asyncio.sleep(1)

    # Twisting poses
    logger.info("Demonstrating twist poses")
    logger.info("Twisting left")
    await dog.pose(lean=0, twist=-1, look=0, extend=0, duration_ms=2000)
    await asyncio.sleep(1)
    
    logger.info("Twisting right")
    await dog.pose(lean=0, twist=1, look=0, extend=0, duration_ms=2000)
    await asyncio.sleep(1)
    
    await dog.reset_body()
    await asyncio.sleep(1)

    # Looking poses
    logger.info("Demonstrating look poses")
    logger.info("Looking up")
    await dog.pose(lean=0, twist=0, look=-1, extend=0, duration_ms=2000)
    await asyncio.sleep(1)
    
    logger.info("Looking down")
    await dog.pose(lean=0, twist=0, look=1, extend=0, duration_ms=2000)
    await asyncio.sleep(1)
    
    await dog.reset_body()
    await asyncio.sleep(1)

    # Extension poses
    logger.info("Demonstrating extension poses")
    logger.info("Squatting down")
    await dog.pose(lean=0, twist=0, look=0, extend=-1, duration_ms=2000)
    await asyncio.sleep(1)
    
    logger.info("Extending up")
    await dog.pose(lean=0, twist=0, look=0, extend=1, duration_ms=2000)
    await asyncio.sleep(1)
    
    await dog.reset_body()
    await asyncio.sleep(1)

async def main():
    """Main function demonstrating various joint movements and poses."""
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

        # Set to stand mode
        logger.info("Setting stand mode")
        dog.set_mode(Go1Mode.STAND)
        await asyncio.sleep(2)  # Wait for mode to take effect
        
        try:
            # Run pose demonstrations
            await demonstrate_direct_poses(dog)
            await asyncio.sleep(1)
            
            await demonstrate_generic_poses(dog)
            logger.info("Pose demonstration completed successfully")
            
        except Exception as e:
            logger.error(f"Error during pose demonstration: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            # Ensure robot returns to neutral pose
            await dog.reset_body()
            await asyncio.sleep(1)
            dog.set_mode(Go1Mode.STAND_DOWN)
            
    except Exception as e:
        logger.error(f"Error initializing robot: {str(e)}")
    finally:
        if 'dog' in locals():
            logger.info("Disconnecting...")
            dog.mqtt.disconnect()

def print_menu():
    """Print available pose demonstrations menu."""
    print("\nAvailable Demonstrations:")
    print("1. Direct Poses (Extend/Squat)")
    print("2. Lean Poses (Left/Right)")
    print("3. Twist Poses (Left/Right)")
    print("4. Look Poses (Up/Down)")
    print("5. Extension Poses (Up/Down)")
    print("6. All Poses")
    print("0. Exit")

async def interactive_main():
    """Interactive main function allowing user to choose demonstrations."""
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
            choice = input("Select a demonstration (0-6): ")

            if choice == "0":
                break

            # Set stand mode before each demonstration
            logger.info("Setting stand mode")
            dog.set_mode(Go1Mode.STAND)
            await asyncio.sleep(2)

            try:
                if choice == "1":
                    await demonstrate_direct_poses(dog)
                elif choice == "2":
                    logger.info("Demonstrating lean poses")
                    await dog.pose(lean=-1, twist=0, look=0, extend=0, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.pose(lean=1, twist=0, look=0, extend=0, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.reset_body()
                elif choice == "3":
                    logger.info("Demonstrating twist poses")
                    await dog.pose(lean=0, twist=-1, look=0, extend=0, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.pose(lean=0, twist=1, look=0, extend=0, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.reset_body()
                elif choice == "4":
                    logger.info("Demonstrating look poses")
                    await dog.pose(lean=0, twist=0, look=-1, extend=0, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.pose(lean=0, twist=0, look=1, extend=0, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.reset_body()
                elif choice == "5":
                    logger.info("Demonstrating extension poses")
                    await dog.pose(lean=0, twist=0, look=0, extend=-1, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.pose(lean=0, twist=0, look=0, extend=1, duration_ms=2000)
                    await asyncio.sleep(1)
                    await dog.reset_body()
                elif choice == "6":
                    await demonstrate_direct_poses(dog)
                    await demonstrate_generic_poses(dog)
                else:
                    print("Invalid choice!")
                    continue

            except Exception as e:
                logger.error(f"Error during demonstration: {e}")
            finally:
                # Return to neutral pose after each demonstration
                await dog.reset_body()
                dog.set_mode(Go1Mode.STAND_DOWN)
                await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if 'dog' in locals():
            logger.info("Disconnecting...")
            dog.mqtt.disconnect()

if __name__ == "__main__":
    try:
        # Use interactive_main() for user input, or main() for demonstration
        asyncio.run(interactive_main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
