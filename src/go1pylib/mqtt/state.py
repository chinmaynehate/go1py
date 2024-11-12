from dataclasses import dataclass, field
from typing import List, Literal, Union
from enum import Enum
import json
from copy import deepcopy

# Define AI mode type
AiMode = Literal["MNFH", "cam1", "cam2", "cam3", "cam4", "cam5"]

@dataclass
class BMSState:
    """Battery Management System state information."""
    version: str = "unknown"
    status: int = 0
    soc: float = 0.0  # State of charge
    current: float = 0.0
    cycle: int = 0
    temps: List[float] = field(default_factory=lambda: [0.0] * 4)
    voltage: float = 0.0
    cell_voltages: List[float] = field(default_factory=lambda: [0.0] * 10)

@dataclass
class SerialNumber:
    """Robot serial number information."""
    product: str = "--"
    id: str = "--"

@dataclass
class Version:
    """Robot version information."""
    hardware: str = "--"
    software: str = "--"

@dataclass
class DistanceWarning:
    """Distance warning information from sensors."""
    front: float = 0.0
    back: float = 0.0
    left: float = 0.0
    right: float = 0.0

@dataclass
class RobotState:
    """Complete robot state information."""
    sn: SerialNumber = field(default_factory=SerialNumber)
    version: Version = field(default_factory=Version)
    temps: List[float] = field(default_factory=lambda: [0.0] * 20)
    mode: int = 0
    gait_type: int = 0
    obstacles: List[int] = field(default_factory=lambda: [255] * 4)
    state: str = "invalid"
    distance_warning: DistanceWarning = field(default_factory=DistanceWarning)

@dataclass
class Go1State:
    """
    Complete state representation of the Go1 robot.
    
    This includes connection status, battery information, and robot state.
    """
    mqtt_connected: bool = False
    manager_on: bool = False
    controller_on: bool = False
    bms: BMSState = field(default_factory=BMSState)
    robot: RobotState = field(default_factory=RobotState)

    def to_dict(self) -> dict:
        """Convert the state to a dictionary representation."""
        return {
            'mqtt_connected': self.mqtt_connected,
            'manager_on': self.manager_on,
            'controller_on': self.controller_on,
            'bms': {
                'version': self.bms.version,
                'status': self.bms.status,
                'soc': self.bms.soc,
                'current': self.bms.current,
                'cycle': self.bms.cycle,
                'temps': self.bms.temps,
                'voltage': self.bms.voltage,
                'cell_voltages': self.bms.cell_voltages,
            },
            'robot': {
                'sn': {
                    'product': self.robot.sn.product,
                    'id': self.robot.sn.id,
                },
                'version': {
                    'hardware': self.robot.version.hardware,
                    'software': self.robot.version.software,
                },
                'temps': self.robot.temps,
                'mode': self.robot.mode,
                'gait_type': self.robot.gait_type,
                'obstacles': self.robot.obstacles,
                'state': self.robot.state,
                'distance_warning': {
                    'front': self.robot.distance_warning.front,
                    'back': self.robot.distance_warning.back,
                    'left': self.robot.distance_warning.left,
                    'right': self.robot.distance_warning.right,
                },
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Go1State':
        """
        Create a Go1State instance from a dictionary.
        
        Args:
            data: Dictionary containing Go1 state data
            
        Returns:
            Go1State instance
        """
        state = cls()
        state.mqtt_connected = data.get('mqtt_connected', False)
        state.manager_on = data.get('manager_on', False)
        state.controller_on = data.get('controller_on', False)
        
        bms_data = data.get('bms', {})
        state.bms = BMSState(
            version=bms_data.get('version', "unknown"),
            status=bms_data.get('status', 0),
            soc=bms_data.get('soc', 0.0),
            current=bms_data.get('current', 0.0),
            cycle=bms_data.get('cycle', 0),
            temps=bms_data.get('temps', [0.0] * 4),
            voltage=bms_data.get('voltage', 0.0),
            cell_voltages=bms_data.get('cell_voltages', [0.0] * 10)
        )
        
        robot_data = data.get('robot', {})
        state.robot = RobotState(
            sn=SerialNumber(
                product=robot_data.get('sn', {}).get('product', "--"),
                id=robot_data.get('sn', {}).get('id', "--")
            ),
            version=Version(
                hardware=robot_data.get('version', {}).get('hardware', "--"),
                software=robot_data.get('version', {}).get('software', "--")
            ),
            temps=robot_data.get('temps', [0.0] * 20),
            mode=robot_data.get('mode', 0),
            gait_type=robot_data.get('gait_type', 0),
            obstacles=robot_data.get('obstacles', [255] * 4),
            state=robot_data.get('state', "invalid"),
            distance_warning=DistanceWarning(
                **robot_data.get('distance_warning', {})
            )
        )
        return state

# Create default state instance
_default_state = Go1State()

def get_go1_state_copy() -> Go1State:
    """
    Get a deep copy of the default Go1 state.
    
    Returns:
        New Go1State instance with default values
    """
    return deepcopy(_default_state)