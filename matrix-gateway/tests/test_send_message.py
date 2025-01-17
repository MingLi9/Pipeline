import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from fastapi import FastAPI
from app.routes.message_routes import router

# Setup test app
app = FastAPI()
app.include_router(router)

mock_client_pool = {}

@pytest.fixture
def client():
    # Patch the client pool to mock its functionality
    with patch("app.clients.client_pool", mock_client_pool):
        yield TestClient(app)

# Todo: FIX TEST
# @pytest.mark.asyncio
# async def test_send_message_success(client):
#     # Mock a bot client
#     mock_client = AsyncMock()
#     mock_client_pool["test_bot"] = mock_client

#     # Send a request to the endpoint
#     response = client.post(
#         "/send",
#         json={
#             "username": "test_bot",
#             "room_id": "test_room",
#             "message": "Hello, world!"
#         }
#     )

#     # Assert response
#     assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
#     assert response.json() == {"message": "Message sent to test_room"}

#     # Verify that room_send was called correctly
#     mock_client.room_send.assert_called_once_with(
#         room_id="test_room",
#         message_type="m.room.message",
#         content={"msgtype": "m.text", "body": "Hello, world!"},
#     )

@pytest.mark.asyncio
async def test_send_message_bot_not_found(client):
    # Ensure no bots are in the client pool
    mock_client_pool.clear()

    # Send a request with a nonexistent bot
    response = client.post(
        "/send",
        json={
            "username": "unknown_bot",
            "room_id": "test_room",
            "message": "Hello, world!"
        }
    )

    # Assert response
    assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
    assert response.json() == {"detail": "Bot not found"}
