from typing import Dict, Callable, Protocol
import struct
import logging
from .state import Go1State
from .topics import SubTopic
from .receivers import bms_receivers, robot_receivers

logger = logging.getLogger(__name__)

class DataView:
    """Class for binary data handling."""
    def __init__(self, buffer: bytes, byte_offset: int = 0, byte_length: int = None):
        self.buffer = buffer
        self.byte_offset = byte_offset
        self.byte_length = byte_length or len(buffer) - byte_offset

    def get_float32(self, byte_offset: int, little_endian: bool = True) -> float:
        """Get a 32-bit float from the buffer."""
        start = self.byte_offset + byte_offset
        return struct.unpack('<f' if little_endian else '>f',
                           self.buffer[start:start + 4])[0]

    def get_uint8(self, byte_offset: int) -> int:
        """Get an 8-bit unsigned integer from the buffer."""
        return self.buffer[self.byte_offset + byte_offset]

    def get_uint16(self, byte_offset: int, little_endian: bool = True) -> int:
        """Get a 16-bit unsigned integer from the buffer."""
        start = self.byte_offset + byte_offset
        return struct.unpack('<H' if little_endian else '>H',
                           self.buffer[start:start + 2])[0]

def message_handler(topic: str, message: bytes, data: Go1State) -> None:
    """
    Process an incoming MQTT message.
    
    Args:
        topic: The MQTT topic the message was received on
        message: The raw message bytes
        data: The current Go1 state to update
    """
    try:
        data_view = DataView(message)
        
        # Get appropriate receiver based on topic
        if topic in bms_receivers:
            receiver = bms_receivers[topic]
            receiver(data, message, data_view)
        elif topic in robot_receivers:
            receiver = robot_receivers[topic]
            receiver(data, message, data_view)
        else:
            logger.debug(f"No receiver for topic: {topic}")
            
    except Exception as e:
        logger.error(f"Error processing message on topic {topic}: {str(e)}")
