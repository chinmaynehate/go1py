import pytest
import asyncio
from unittest.mock import AsyncMock, Mock
from go1pylib import Go1, Go1Mode

@pytest.fixture
def mock_mqtt():
    """Fixture to create a mock MQTT client."""
    mock_mqtt = Mock()
    mock_mqtt.connect = Mock()
    mock_mqtt.subscribe = Mock()
    mock_mqtt.update_speed = Mock()
    mock_mqtt.send_movement_command = AsyncMock()
    mock_mqtt.send_led_command = Mock()
    mock_mqtt.send_mode_command = Mock()
    return mock_mqtt

@pytest.fixture
def go1_robot(mock_mqtt):
    """Fixture to initialize a Go1 robot instance with mocked MQTT client."""
    robot = Go1()
    robot.mqtt = mock_mqtt  # Inject mock MQTT client
    return robot

@pytest.mark.asyncio
async def test_go_forward(go1_robot):
    await go1_robot.go_forward(speed=0.5, duration_ms=1000)
    go1_robot.mqtt.update_speed.assert_called_once_with(0, 0, 0, 0.5)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(1000)

@pytest.mark.asyncio
async def test_go_backward(go1_robot):
    await go1_robot.go_backward(speed=0.5, duration_ms=1000)
    go1_robot.mqtt.update_speed.assert_called_once_with(0, 0, 0, -0.5)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(1000)

@pytest.mark.asyncio
async def test_go_left(go1_robot):
    await go1_robot.go_left(speed=0.3, duration_ms=500)
    go1_robot.mqtt.update_speed.assert_called_once_with(-0.3, 0, 0, 0)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(500)

@pytest.mark.asyncio
async def test_go_right(go1_robot):
    await go1_robot.go_right(speed=0.3, duration_ms=500)
    go1_robot.mqtt.update_speed.assert_called_once_with(0.3, 0, 0, 0)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(500)

@pytest.mark.asyncio
async def test_turn_left(go1_robot):
    await go1_robot.turn_left(speed=0.4, duration_ms=750)
    go1_robot.mqtt.update_speed.assert_called_once_with(0, -0.4, 0, 0)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(750)

@pytest.mark.asyncio
async def test_turn_right(go1_robot):
    await go1_robot.turn_right(speed=0.4, duration_ms=750)
    go1_robot.mqtt.update_speed.assert_called_once_with(0, 0.4, 0, 0)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(750)

@pytest.mark.asyncio
async def test_pose(go1_robot):
    await go1_robot.pose(lean=0.1, twist=0.2, look=-0.1, extend=0.5, duration_ms=1200)
    go1_robot.mqtt.update_speed.assert_called_once_with(0.1, 0.2, -0.1, 0.5)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(1200)

@pytest.mark.asyncio
async def test_extend_up(go1_robot):
    await go1_robot.extend_up(speed=0.6, duration_ms=1500)
    go1_robot.mqtt.update_speed.assert_called_once_with(0, 0, 0, 0.6)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(1500)

@pytest.mark.asyncio
async def test_squat_down(go1_robot):
    await go1_robot.squat_down(speed=0.6, duration_ms=1500)
    go1_robot.mqtt.update_speed.assert_called_once_with(0, 0, 0, -0.6)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(1500)

@pytest.mark.asyncio
async def test_reset_body(go1_robot):
    await go1_robot.reset_body()
    go1_robot.mqtt.update_speed.assert_called_once_with(0, 0, 0, 0)
    go1_robot.mqtt.send_movement_command.assert_called_once_with(1000)

def test_set_led_color(go1_robot):
    go1_robot.set_led_color(255, 0, 0)
    go1_robot.mqtt.send_led_command.assert_called_once_with(255, 0, 0)

def test_set_mode(go1_robot):
    go1_robot.set_mode(Go1Mode.WALK)
    go1_robot.mqtt.send_mode_command.assert_called_once_with(Go1Mode.WALK)

@pytest.mark.asyncio
async def test_wait(go1_robot):
    start_time = asyncio.get_event_loop().time()
    await go1_robot.wait(1000)  # 1 second
    end_time = asyncio.get_event_loop().time()
    assert (end_time - start_time) >= 1
