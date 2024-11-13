import asyncio
import logging
import time
from typing import Tuple
from go1pylib.go1 import Go1
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LEDController:
    def __init__(self, dog: Go1):
        self.dog = dog
        self.running = False

    async def pulse(self, r: int, g: int, b: int, duration_s: float = 2.0):
        """Pulse LED from off to full brightness and back."""
        steps = 50
        for i in range(steps):
            # Fade in
            brightness = i / steps
            self.dog.set_led_color(
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            )
            await asyncio.sleep(duration_s / (2 * steps))
            
        for i in range(steps):
            # Fade out
            brightness = 1 - (i / steps)
            self.dog.set_led_color(
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            )
            await asyncio.sleep(duration_s / (2 * steps))

    async def rainbow_cycle(self, duration_s: float = 5.0):
        """Cycle through rainbow colors."""
        steps = 100
        for i in range(steps):
            hue = i / steps
            r, g, b = self._hsv_to_rgb(hue, 1.0, 1.0)
            self.dog.set_led_color(r, g, b)
            await asyncio.sleep(duration_s / steps)

    async def police_lights(self, duration_s: float = 5.0):
        """Alternate between red and blue like police lights."""
        cycles = int(duration_s * 2)  # 2 changes per second
        for _ in range(cycles):
            if not self.running:
                break
            self.dog.set_led_color(255, 0, 0)  # Red
            await asyncio.sleep(0.25)
            self.dog.set_led_color(0, 0, 255)  # Blue
            await asyncio.sleep(0.25)

    async def strobe(self, r: int, g: int, b: int, duration_s: float = 5.0):
        """Create a strobe light effect."""
        cycles = int(duration_s * 10)  # 10 flashes per second
        for _ in range(cycles):
            if not self.running:
                break
            self.dog.set_led_color(r, g, b)
            await asyncio.sleep(0.05)
            self.dog.set_led_color(0, 0, 0)
            await asyncio.sleep(0.05)

    async def random_colors(self, duration_s: float = 5.0):
        """Display random colors."""
        cycles = int(duration_s * 2)  # 2 changes per second
        for _ in range(cycles):
            if not self.running:
                break
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.dog.set_led_color(r, g, b)
            await asyncio.sleep(0.5)

    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
        """
        Convert HSV color to RGB.
        
        Args:
            h: Hue (0-1)
            s: Saturation (0-1)
            v: Value (0-1)
            
        Returns:
            Tuple of (r, g, b) values (0-255)
        """
        if s == 0.0:
            v_int = int(v * 255)
            return (v_int, v_int, v_int)

        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6

        if i == 0:
            return (int(v * 255), int(t * 255), int(p * 255))
        if i == 1:
            return (int(q * 255), int(v * 255), int(p * 255))
        if i == 2:
            return (int(p * 255), int(v * 255), int(t * 255))
        if i == 3:
            return (int(p * 255), int(q * 255), int(v * 255))
        if i == 4:
            return (int(t * 255), int(p * 255), int(v * 255))
        return (int(v * 255), int(p * 255), int(q * 255))

def print_menu():
    """Print available LED effects menu."""
    print("\nAvailable LED Effects:")
    print("1. Pulse (fade in/out)")
    print("2. Rainbow Cycle")
    print("3. Police Lights")
    print("4. Strobe Light")
    print("5. Random Colors")
    print("6. Custom Color")
    print("0. Exit")

async def interactive_main():
    """Interactive main function allowing user to choose effects."""
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

        # Create LED controller
        led = LEDController(dog)
        led.running = True

        while True:
            print_menu()
            choice = input("Select an effect (0-6): ")

            if choice == "0":
                break
            elif choice == "1":
                color = input("Enter color (r,g,b): ").split(",")
                await led.pulse(int(color[0]), int(color[1]), int(color[2]))
            elif choice == "2":
                await led.rainbow_cycle()
            elif choice == "3":
                await led.police_lights()
            elif choice == "4":
                color = input("Enter color (r,g,b): ").split(",")
                await led.strobe(int(color[0]), int(color[1]), int(color[2]))
            elif choice == "5":
                await led.random_colors()
            elif choice == "6":
                color = input("Enter color (r,g,b): ").split(",")
                dog.set_led_color(int(color[0]), int(color[1]), int(color[2]))
            else:
                print("Invalid choice!")

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if 'dog' in locals():
            dog.set_led_color(0, 0, 0)  # Turn off LED
            dog.mqtt.disconnect()

if __name__ == "__main__":
    try:
        asyncio.run(interactive_main())
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
