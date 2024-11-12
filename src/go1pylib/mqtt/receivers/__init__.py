"""Message receivers for different types of Go1 robot data."""

from .bms import bms_receivers
from .robot import robot_receivers

__all__ = ["bms_receivers", "robot_receivers"]