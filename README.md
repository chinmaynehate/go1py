
# go1pylib: Python Library for Go1 Robot Control

[![PyPI version](https://img.shields.io/pypi/v/go1pylib)](https://pypi.org/project/go1pylib/) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT) ![Python Versions](https://img.shields.io/pypi/pyversions/go1pylib)

go1pylib is a Python library designed for controlling the Go1 robot, providing high-level methods for robot movement, state management, and collision avoidance. With built-in functionality for MQTT communication and control modes, go1pylib is ideal for both development and research use in robotics applications.

## Features

- **Robot Control**: Seamlessly control Go1's movements, including forward, backward, turns, and various pose adjustments.
- **Collision Avoidance**: Built-in methods for safe navigation with customizable thresholds for obstacle detection.
- **Battery Monitoring**: Real-time battery status feedback with configurable LED indicators based on battery levels.
- **LED Control**: Control LED colors for custom feedback based on robot state or user-defined actions.
- **MQTT Communication**: Reliable MQTT communication interface for Go1 state management and control.
- **Multiple Control Modes**: Switch between modes such as WALK and STAND for different application scenarios.

## Installation

Install the latest version of go1pylib using pip:

```bash
pip install go1pylib
```

## Usage

Here's a quick example demonstrating basic usage:

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

Examples for controlling the robot, collision avoidance, and LED control can be found in the `examples` directory.

## Project Structure

```
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

Complete documentation can be found [here](https://github.com/chinmaynehate/go1pylib).

## Contributing

Contributions are welcome! Please see our [contributing guidelines](https://github.com/chinmaynehate/go1pylib/blob/main/CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.