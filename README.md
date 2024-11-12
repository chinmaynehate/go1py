
![go1pylib](go1.gif)
# go1pylib: Python Library for Go1 Robot Control

![PyPI version](https://img.shields.io/pypi/v/go1pylib) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) ![Python Versions](https://img.shields.io/pypi/pyversions/go1pylib)

go1pylib is a Python library designed for controlling the Go1 robot, providing high-level methods for robot movement, state management, and collision avoidance. With built-in functionality for MQTT communication and control modes, go1pylib is ideal for both development and research in robotics.

## Features

- **Robot Control**: Control Go1's movements including forward, backward, turns, and pose adjustments.
- **Collision Avoidance**: Includes safe navigation with customizable obstacle detection thresholds.
- **Battery Monitoring**: Real-time battery status with configurable LED indicators.
- **LED Control**: Customizable LED color control based on robot state or custom feedback.
- **MQTT Communication**: Reliable MQTT communication for Go1 state management and control.
- **Multiple Control Modes**: Switch modes such as WALK and STAND for various scenarios.

## Installation

Install the latest version of go1pylib with pip:

```bash
pip install go1pylib
```

## Usage

Here's an example to get started:

```python
import asyncio
from go1pylib import Go1, Go1Mode

async def main():
    robot = Go1()
    robot.init()  # Connect to the robot

    # Set to WALK mode and move forward
    robot.set_mode(Go1Mode.WALK)
    await robot.go_forward(speed=0.3, duration_ms=1000)

    # Check battery status
    battery_level = robot.get_battery_level()
    print(f"Battery Level: {battery_level}%")

    # Stop and disconnect
    robot.set_mode(Go1Mode.STAND_DOWN)
    robot.disconnect()

asyncio.run(main())
```

## Examples

Find more examples in the `examples` directory for controlling the robot, collision avoidance, and LED control.

## Project Structure

```plaintext
go1pylib/
├── examples/
│   ├── move_forward.py
│   ├── dance.py
│   └── avoid_obstacles.py
├── src/
│   └── go1pylib/
│       ├── go1.py
│       ├── mqtt/
│       ├── state.py
│       └── ...
├── tests/
└── README.md
```

## Documentation

Full documentation can be found [here](https://github.com/chinmaynehate/go1pylib).

## Contributing

Contributions are welcome! Check out our [contributing guidelines](https://github.com/chinmaynehate/go1pylib/blob/main/CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/chinmaynehate/go1pylib/blob/main/LICENSE) file for details.