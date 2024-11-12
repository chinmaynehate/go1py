"""
Go1Py - Python Library for Go1 Robot Control

This library provides a Python interface for controlling the Go1 quadruped robot.
"""

from .go1 import Go1, Go1Mode
from .mqtt.state import Go1State

__version__ = "0.1.1"
__author__ = "Your Name"
__license__ = "MIT"

# Export main classes for easier imports
__all__ = ["Go1", "Go1Mode", "Go1State"]