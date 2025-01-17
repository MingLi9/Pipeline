from unittest.mock import AsyncMock, patch, MagicMock
import pytest
from app.clients import (
    create_client, 
    start_sync, 
    process_pending_invites, 
    join_room, 
    on_invite_event,
    client_pool
)
from app.utils.event_callbacks import (
    message_listener
)
from nio import AsyncClient, InviteEvent, RoomMessageText

@pytest.mark.asyncio
@patch("app.clients.HOMESERVER_URL", "http://your-homeserver-url")
@patch("app.clients.AsyncClient")
@patch("app.clients.on_invite_event")
@patch("app.clients.message_listener")
async def test_create_client(mock_message_listener, mock_on_invite_event, mock_async_client):
    # Mock the AsyncClient instance
    mock_client_instance = AsyncMock()
    mock_client_instance.user_id = "bot_user"
    mock_async_client.return_value = mock_client_instance

    # Mock the login response
    mock_client_instance.login.return_value = AsyncMock(access_token="test_token")

    username = "bot_user"
    password = "bot_pass"

    # Call the function under test
    client = await create_client(username, password)

    # Assertions
    mock_async_client.assert_called_once_with("http://your-homeserver-url", username)
    mock_client_instance.login.assert_called_once_with(password)

    # Verify client is added to the client_pool
    assert client_pool["bot_user"] == client

    # Verify the callbacks are registered
    mock_client_instance.add_event_callback.assert_any_call(mock_on_invite_event, InviteEvent)
    mock_client_instance.add_event_callback.assert_any_call(mock_message_listener, RoomMessageText)

    # Ensure the returned client is the one created
    assert client == mock_client_instance

@pytest.mark.asyncio
@patch("app.clients.process_pending_invites")
async def test_start_sync(mock_process_pending_invites):
    client = AsyncMock()
    client.user_id = "bot_user"

    with patch("asyncio.create_task", return_value=MagicMock()) as mock_create_task:
        await start_sync(client)

        mock_create_task.assert_called_once()
        mock_process_pending_invites.assert_awaited_once_with(client)


@pytest.mark.asyncio
async def test_process_pending_invites_no_invites():
    client = AsyncMock()
    client.invited_rooms = {}

    await process_pending_invites(client)

    client.join.assert_not_called()


@pytest.mark.asyncio
async def test_process_pending_invites_with_invites():
    client = AsyncMock()
    client.invited_rooms = {"room_1": AsyncMock()}

    await process_pending_invites(client)

    client.join.assert_awaited_once_with("room_1")


@pytest.mark.asyncio
async def test_join_room_success():
    client = AsyncMock()
    room_id = "room_1"

    await join_room(client, room_id)

    client.join.assert_awaited_once_with(room_id)


@pytest.mark.asyncio
async def test_join_room_failure():
    client = AsyncMock()
    room_id = "room_1"
    client.join.side_effect = Exception("Join error")

    await join_room(client, room_id)

    client.join.assert_awaited_once_with(room_id)


@pytest.mark.asyncio
async def test_on_invite_event_success():
    client = AsyncMock()
    event = AsyncMock()
    event.room_id = "room_1"
    event.own_user_id = "bot_user"

    # Mock the client pool
    client_pool["bot_user"] = client

    await on_invite_event(event, client)

    client.join.assert_awaited_once_with("room_1")


@pytest.mark.asyncio
async def test_on_invite_event_client_not_found():
    client = AsyncMock()
    event = AsyncMock()
    event.room_id = "room_1"
    event.own_user_id = "unknown_user"

    await on_invite_event(event, client)

    client.join.assert_not_called()


@pytest.mark.asyncio
async def test_on_invite_event_join_failure():
    client = AsyncMock()
    event = AsyncMock()
    event.room_id = "room_1"
    event.own_user_id = "bot_user"
    client.join.side_effect = Exception("Join error")

    client_pool["bot_user"] = client

    await on_invite_event(event, client)

    client.join.assert_awaited_once_with("room_1")


@pytest.mark.asyncio
@patch("app.clients.HOMESERVER_URL", "http://your-homeserver-url")
@patch("app.clients.AsyncClient")
async def test_create_client_callbacks_and_client_pool(mock_async_client):
    # Mock AsyncClient instance
    mock_client_instance = AsyncMock()
    mock_client_instance.user_id = "bot_user"
    mock_async_client.return_value = mock_client_instance

    # Mock the login response
    mock_client_instance.login.return_value = AsyncMock(access_token="test_token")

    username = "bot_user"
    password = "bot_pass"

    # Call the function
    client = await create_client(username, password)

    # Ensure client is added to client_pool
    assert "bot_user" in client_pool
    assert client_pool["bot_user"] == mock_client_instance

    # Check that add_event_callback was called with the correct arguments
    mock_client_instance.add_event_callback.assert_any_call(on_invite_event, InviteEvent)
    mock_client_instance.add_event_callback.assert_any_call(message_listener, RoomMessageText)

    # Ensure the returned client is the one created
    assert client == mock_client_instance
