
<div align="center">

![go1pylib](go1.gif)

# go1pylib: Python Library for Go1 Robot Control

[![PyPI version](https://badge.fury.io/py/go1pylib.svg)](https://pypi.org/project/go1pylib/) 
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) 
![Python Versions](https://img.shields.io/pypi/pyversions/go1pylib)

</div>

go1pylib is a Python library designed for controlling the Go1 robot, providing high-level methods for robot movement, state management, and collision avoidance. With built-in functionality for MQTT communication and control modes, go1pylib is ideal for both development and research in robotics.

---

## :star2: Features

- **Robot Control**: Control Go1's movements including forward, backward, turns, and pose adjustments.
- **Collision Avoidance**: Includes safe navigation with customizable obstacle detection thresholds.
- **Battery Monitoring**: Real-time battery status with configurable LED indicators.
- **LED Control**: Customizable LED color control based on robot state or custom feedback.
- **MQTT Communication**: Reliable MQTT communication for Go1 state management and control.
- **Multiple Control Modes**: Switch modes such as WALK and STAND for various scenarios.

## :rocket: Installation

Install the latest version of go1pylib with pip:

```bash
pip install go1pylib
```

## :computer: Usage

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

## :file_folder: Examples

Find more examples in the `examples` directory for controlling the robot, collision avoidance, and LED control.

## :file_cabinet: Project Structure

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

## :books: Documentation

Full documentation can be found [here](https://chinmaynehate.github.io/go1pylib/).

## :handshake: Contributing

Contributions are welcome! Check out our [contributing guidelines](https://github.com/chinmaynehate/go1pylib/blob/main/CONTRIBUTING.md) for more information.

## :warning: License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/chinmaynehate/go1pylib/blob/main/LICENSE) file for details.

## :gem: Acknowledgments

Special thanks to:

- [go1-js by dbaldwin](https://github.com/dbaldwin/go1-js)
- [YushuTechUnitreeGo1 by MAVProxyUser](https://github.com/MAVProxyUser/YushuTechUnitreeGo1) 
- [Unitree Go1 Educational Documentation](https://unitree-docs.readthedocs.io/en/latest/get_started/Go1_Edu.html)

Thank you to all contributors who made this project possible!
