from unittest.mock import AsyncMock, patch
import pytest
from app.utils.event_callbacks import message_listener
from nio import RoomMessageText, MatrixRoom


class MockRoom(MatrixRoom):
    def __init__(self, room_id="!room123:matrix.org", own_user_id="@bot123:matrix.org"):
        super().__init__(room_id=room_id, own_user_id=own_user_id)

    @property
    def display_name(self):
        return "Test Room"


class MockEvent(RoomMessageText):
    def __init__(self, sender="@user456:matrix.org", body="Hello, bot!", timestamp=1695742940000):
        source = {
            "content": {
                "body": body,
                "msgtype": "m.text",
            },
            "sender": sender,
            "origin_server_ts": timestamp,
            "event_id": "$event12345:matrix.org",  # Add a mock event_id
        }
        super().__init__(
            body=body,
            formatted_body=None,
            format=None,
            source=source,
        )
        self.server_timestamp = timestamp


@patch("app.utils.event_callbacks.send_to_gateway", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_message_listener_valid_event(mock_send_to_gateway):
    """Test message_listener with a valid event."""
    # Mock return value of send_to_gateway
    mock_send_to_gateway.return_value = {"status": "success"}

    room = MockRoom()
    event = MockEvent()

    await message_listener(room, event)

    mock_send_to_gateway.assert_called_once_with(
        "/chat_message",
        {
            "room_id": "!room123:matrix.org",
            "room_name": "Test Room",
            "sender": "@user456:matrix.org",
            "receiver": "@bot123:matrix.org",
            "message": "Hello, bot!",
            "timestamp": 1695742940000,
        }
    )


@patch("app.utils.event_callbacks.send_to_gateway", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_message_listener_same_sender_receiver(mock_send_to_gateway):
    """Test message_listener skips when sender and receiver are the same."""
    room = MockRoom()
    event = MockEvent(sender="@bot123:matrix.org")  # Same as room's own_user_id

    await message_listener(room, event)

    mock_send_to_gateway.assert_not_called()


@patch("app.utils.event_callbacks.send_to_gateway", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_message_listener_invalid_event_type(mock_send_to_gateway):
    """Test message_listener skips when event is not RoomMessageText."""
    room = MockRoom()
    event = object()  # Invalid event type

    await message_listener(room, event)

    mock_send_to_gateway.assert_not_called()


@patch("app.utils.event_callbacks.send_to_gateway", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_message_listener_invalid_room_type(mock_send_to_gateway):
    """Test message_listener skips when room is not MatrixRoom."""
    room = object()  # Invalid room type
    event = MockEvent()

    await message_listener(room, event)

    mock_send_to_gateway.assert_not_called()
