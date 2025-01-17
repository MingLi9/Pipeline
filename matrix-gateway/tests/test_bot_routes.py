from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import pytest
from app.main import app

# Create a test client for FastAPI
client = TestClient(app)

# Mock for client_pool
mock_client_pool = {}


@pytest.fixture
def setup_mock_client_pool():
    """
    Fixture to patch the client_pool with a mock dictionary for each test.
    Ensures that operations in the application modify mock_client_pool.
    """
    with patch("app.clients.client_pool", mock_client_pool):
        with patch("app.routes.bot_routes.client_pool", mock_client_pool):
            yield


@pytest.mark.asyncio
@patch("app.routes.bot_routes.create_client", new_callable=AsyncMock)
@patch("app.routes.bot_routes.start_sync", new_callable=AsyncMock)
async def test_add_bot(mock_start_sync, mock_create_client, setup_mock_client_pool):
    """
    Test adding a bot successfully.
    Ensures the create_client and start_sync functions are called as expected.
    """
    response = client.post("/bots/add", json={"username": "bot1", "password": "pass1"})
    assert response.status_code == 200
    assert response.json()["message"] == "Bot bot1 added"

    # Verify mocks were called with expected arguments
    mock_create_client.assert_called_once_with("bot1", "pass1")
    mock_start_sync.assert_called_once()


@pytest.mark.asyncio
async def test_remove_bot_success(setup_mock_client_pool):
    """
    Test successfully removing a bot.
    Ensures the bot is removed from the client pool and the close method is called.
    """
    # Mock adding a bot to the client pool
    mock_client = AsyncMock()
    mock_client_pool["bot1"] = mock_client

    print(f"Before removal (in test): {mock_client_pool}")

    # Send a request to remove the bot
    response = client.post("/bots/remove", json={"username": "bot1"})

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"message": "Bot bot1 removed"}

    print(f"After removal (in test): {mock_client_pool}")

    # Verify the bot was removed from the pool
    assert "bot1" not in mock_client_pool, f"Expected bot1 to be removed from the pool, but it remains: {mock_client_pool}"

    # Verify the bot's `close` method was called
    mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_remove_bot_not_found(setup_mock_client_pool):
    """
    Test removing a bot that does not exist in the client pool.
    Ensures the response indicates the bot was not found.
    """
    # Ensure the client pool is empty
    mock_client_pool.clear()

    # Send a request to remove a non-existent bot
    response = client.post("/bots/remove", json={"username": "unknown_bot"})

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"message": "Bot not found"}


@patch("app.routes.bot_routes.create_client", new_callable=AsyncMock)
@patch("app.routes.bot_routes.start_sync", new_callable=AsyncMock)
@pytest.mark.asyncio
async def test_add_bot_already_exists(mock_start_sync, mock_create_client, setup_mock_client_pool):
    """
    Test attempting to add a bot that already exists in the client pool.
    Ensures that no new client is created or started and the appropriate message is returned.
    """
    # Mock adding a bot to the client pool
    mock_client = AsyncMock()
    mock_client_pool["bot1"] = mock_client

    # Attempt to add the same bot again
    response = client.post("/bots/add", json={"username": "bot1", "password": "pass1"})

    # Assert response
    assert response.status_code == 200
    assert response.json() == {"message": "Bot already exists"}

    # Verify that create_client and start_sync were not called
    mock_create_client.assert_not_called()
    mock_start_sync.assert_not_called()
