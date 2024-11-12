from typing import Dict, Callable
import struct
import logging
from ..state import Go1State
from ..topics import BmsSubTopic
from dataclasses import dataclass

logger = logging.getLogger(__name__)

class BmsReceiver:
    """Handler for Battery Management System (BMS) messages."""
    
    @staticmethod
    def handle_bms_state(data: Go1State, message: bytes, data_view: 'DataView') -> None:
        """
        Process BMS state message and update Go1State.
        
        Args:
            data: Current Go1 state to update
            message: Raw message bytes
            data_view: DataView instance for parsing binary data
            
        The BMS state message contains:
        - Version (2 bytes)
        - Status (1 byte)
        - State of Charge (1 byte)
        - Current (4 bytes, signed int)
        - Cycle count (2 bytes)
        - Temperatures (4 bytes)
        - Cell voltages (20 bytes, 10 cells * 2 bytes each)
        """
        try:
            # Version (first two bytes as major.minor)
            data.bms.version = f"{data_view.get_uint8(0)}.{data_view.get_uint8(1)}"
            
            # Status and SoC
            data.bms.status = data_view.get_uint8(2)
            data.bms.soc = data_view.get_uint8(3)
            
            # Current (signed 32-bit integer)
            data.bms.current = struct.unpack('<i', message[4:8])[0]
            
            # Cycle count (16-bit unsigned integer)
            data.bms.cycle = data_view.get_uint16(8, little_endian=True)
            
            # Temperature readings
            data.bms.temps = [
                data_view.get_uint8(10),
                data_view.get_uint8(11),
                data_view.get_uint8(12),
                data_view.get_uint8(13)
            ]
            
            # Cell voltages (10 cells)
            data.bms.cell_voltages = [
                data_view.get_uint16(14 + i * 2, little_endian=True)
                for i in range(10)
            ]
            
            # Total voltage is sum of cell voltages
            data.bms.voltage = sum(data.bms.cell_voltages)
            
        except Exception as e:
            logger.error(f"Error processing BMS state message: {str(e)}")
            # Keep previous values in case of error
            return

# Create receiver dictionary mapping topics to handler methods
bms_receivers: Dict[BmsSubTopic, Callable] = {
    BmsSubTopic.BMS_STATE: BmsReceiver.handle_bms_state
}