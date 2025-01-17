from unittest.mock import AsyncMock, patch
import pytest
from app.clients import start_sync

@patch("app.clients.AsyncClient")
@pytest.mark.asyncio
async def test_start_sync(mock_client_class):
    # Mock the AsyncClient instance
    mock_client = AsyncMock()
    mock_client_class.return_value = mock_client

    # Mock `sync_forever` to prevent it from running indefinitely
    mock_client.sync_forever = AsyncMock()

    # Mock `invited_rooms` to simulate pending invites
    mock_client.invited_rooms = {
        "!room123:matrix.org": "Room 123",
        "!room456:matrix.org": "Room 456"
    }

    # Call start_sync
    await start_sync(mock_client)

    # Verify `sync_forever` was called
    mock_client.sync_forever.assert_called_once_with(timeout=30000)
