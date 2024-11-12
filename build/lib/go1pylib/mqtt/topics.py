from enum import Enum
from typing import Union, List, Optional

class BmsSubTopic(str, Enum):
    """Topics for Battery Management System (BMS) messages."""
    BMS_STATE = "bms/state"

class FirmwareSubTopic(str, Enum):
    """Topics for firmware-related messages."""
    FIRMWARE_VERSION = "firmware/version"

class PubTopic(str, Enum):
    """Topics for publishing messages to the robot."""
    CONTROLLER_ACTION = "controller/action"
    CONTROLLER_STICK = "controller/stick"
    PROGRAMMING_CODE = "programming/code"

# Define union type for subscription topics
SubTopic = Union[BmsSubTopic, FirmwareSubTopic]

# Optional: Create a helper class for topic validation and management
class Topics:
    """Helper class for managing MQTT topics."""
    
    @staticmethod
    def is_valid_sub_topic(topic: str) -> bool:
        """
        Check if a topic is a valid subscription topic.
        
        Args:
            topic: Topic string to validate
            
        Returns:
            bool: Whether the topic is valid
        """
        try:
            return (topic in BmsSubTopic._value2member_map_ or 
                   topic in FirmwareSubTopic._value2member_map_)
        except ValueError:
            return False

    @staticmethod
    def is_valid_pub_topic(topic: str) -> bool:
        """
        Check if a topic is a valid publish topic.
        
        Args:
            topic: Topic string to validate
            
        Returns:
            bool: Whether the topic is valid
        """
        try:
            return topic in PubTopic._value2member_map_
        except ValueError:
            return False

    @staticmethod
    def get_sub_topics() -> List[str]:  # Changed from list[str] to List[str]
        """
        Get list of all subscription topics.
        
        Returns:
            List of subscription topic strings
        """
        return ([topic.value for topic in BmsSubTopic] + 
                [topic.value for topic in FirmwareSubTopic])

    @staticmethod
    def get_pub_topics() -> List[str]:  # Changed from list[str] to List[str]
        """
        Get list of all publish topics.
        
        Returns:
            List of publish topic strings
        """
        return [topic.value for topic in PubTopic]
