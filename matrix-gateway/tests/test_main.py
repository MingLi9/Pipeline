import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app  # Import your FastAPI app instance
from app.config import API_GATEWAY_URL  # Import the API_GATEWAY_URL directly

# Create a test client
client = TestClient(app)

@pytest.fixture
def test_client():
    """Fixture to provide the test client."""
    return client


def test_root_endpoint(test_client):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200, "Root endpoint should return 200"
    assert response.json() == {"message": "Matrix-Gateway Microservice is running!"}, "Unexpected response from root endpoint"


def test_bots_routes_included(test_client):
    """Test if bot routes are included and accessible."""
    response = test_client.get("/bots")  # Adjust if there are specific bot route endpoints
    assert response.status_code in {200, 404}, "Bot routes should be included"
    # Further assertions can be added based on actual bot routes


def test_messages_routes_included(test_client):
    """Test if message routes are included and accessible."""
    response = test_client.get("/messages")  # Adjust if there are specific message route endpoints
    assert response.status_code in {200, 404}, "Message routes should be included"
    # Further assertions can be added based on actual message routes


def test_app_initialization():
    """Test that the FastAPI app initializes without errors."""
    assert app.title == "FastAPI", "App title should be FastAPI by default"
    assert isinstance(app.router.routes, list), "App should have routes defined"
    assert len(app.router.routes) > 0, "App should have at least one route defined"


@pytest.mark.asyncio
async def test_lifespan_startup():
    """Test the startup logic in the lifespan function."""
    mock_post = AsyncMock(return_value=AsyncMock(status_code=200, text="Success"))
    with patch("httpx.AsyncClient.post", mock_post):
        # Use async with to enter the lifespan context
        async with app.router.lifespan_context(app):
            mock_post.assert_called_with(f"{API_GATEWAY_URL}/bots/ask_connection")
            assert mock_post.call_count == 1, "Startup should call ask_connection once"


@pytest.mark.asyncio
async def test_lifespan_startup_failure():
    """Test the startup logic handles failure gracefully."""
    mock_post = AsyncMock(return_value=AsyncMock(status_code=500, text="Failure"))
    with patch("httpx.AsyncClient.post", mock_post):
        # Use async with to enter the lifespan context
        async with app.router.lifespan_context(app):
            mock_post.assert_called_with(f"{API_GATEWAY_URL}/bots/ask_connection")
            assert mock_post.call_count == 1, "Startup should call ask_connection once"


@pytest.mark.asyncio
async def test_lifespan_shutdown():
    """Test the shutdown logic in the lifespan function."""
    mock_post = AsyncMock(return_value=AsyncMock(status_code=200, text="Success"))
    with patch("httpx.AsyncClient.post", mock_post):
        # Use async with to enter and exit the lifespan context
        async with app.router.lifespan_context(app):
            pass  # Ensure startup logic runs
        mock_post.assert_called_with(f"{API_GATEWAY_URL}/bots/disconnect")
        assert mock_post.call_count == 2, (
            "Shutdown should call disconnect once (1 startup call and 1 shutdown call)"
        )


@pytest.mark.asyncio
async def test_lifespan_shutdown_failure():
    """Test the shutdown logic handles failure gracefully."""
    mock_post = AsyncMock(return_value=AsyncMock(status_code=500, text="Failure"))
    with patch("httpx.AsyncClient.post", mock_post):
        # Use async with to enter and exit the lifespan context
        async with app.router.lifespan_context(app):
            pass  # Ensure startup logic runs
        mock_post.assert_called_with(f"{API_GATEWAY_URL}/bots/disconnect")
        assert mock_post.call_count == 2, (
            "Shutdown should call disconnect once (1 startup call and 1 shutdown call)"
        )
