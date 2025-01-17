import os
import pytest
import asyncio
import json
from dotenv import load_dotenv
from nats.aio.client import Client as NATS
from aiohttp.test_utils import TestClient, TestServer, loop_context
from flask import Flask, jsonify, request


# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def event_loop():
    # Create an event loop for the session
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

class MockMatrixGateway:
    def __init__(self):
        self.received_requests = []

    async def handle_add_bot(self, request):
        self.received_requests.append({
            "url": str(request.url),
            "data": await request.json()
        })
        return jsonify({"message": "Bot added successfully"}), 200

    async def handle_send_message(self, request):
        self.received_requests.append({
            "url": str(request.url),
            "data": await request.json()
        })
        return jsonify({"message": "Message sent successfully"}), 200

@pytest.fixture
def mock_matrix_gateway():
    app = Flask(__name__)
    mock_gateway = MockMatrixGateway()

    @app.route('/bots/add', methods=['POST'])
    def add_bot():
        return asyncio.run(mock_gateway.handle_add_bot(request))

    @app.route('/messages/send', methods=['POST'])
    def send_message():
        return asyncio.run(mock_gateway.handle_send_message(request))

    return app, mock_gateway

@pytest.fixture
def nats_client(event_loop):
    nc = NATS()

    async def connect():
        await nc.connect(servers=["nats://localhost:4222"])
        return nc

    client = event_loop.run_until_complete(connect())
    yield client
    event_loop.run_until_complete(client.close())

@pytest.mark.asyncio
async def test_matrix_login_integration(mock_matrix_gateway, nats_client):
    app, gateway = mock_matrix_gateway

    # Use Flask's test client
    with app.test_client() as client:
        # Simulate NATS message
        await nats_client.publish(
            "bots.connection",
            json.dumps({
                "event_id": "12345",
                "timestamp": "2025-01-09T12:00:00Z",
                "platform": "Matrix",
                "service": "matrix-login",
                "event_type": "post",
                "actor": "Test Actor",
                "payload": json.dumps({
                    "username": "test_user",
                    "password": "test_pass"
                })
            }).encode()
        )

        # Allow async tasks to process
        await asyncio.sleep(1)

        # Simulate a POST request to Flask
        response = client.post(
            "/bots/add",
            json={"username": "test_user", "password": "test_pass"}
        )

        assert response.status_code == 200
        assert len(gateway.received_requests) == 1
        request_data = gateway.received_requests[0]
        assert request_data["url"].endswith("/bots/add")
        assert request_data["data"]["username"] == "test_user"
        assert request_data["data"]["password"] == "test_pass"

@pytest.mark.asyncio
async def test_matrix_message_integration(mock_matrix_gateway, nats_client):
    app, gateway = mock_matrix_gateway

    async with TestClient(TestServer(app)) as client:
        await nats_client.publish(
            "chat.messages",
            json.dumps({
                "event_id": "12345",
                "timestamp": "2025-01-09T12:00:00Z",
                "platform": "Matrix",
                "service": "matrix-message",
                "event_type": "post",
                "actor": "Test Actor",
                "payload": json.dumps({
                    "room_id": "test_room",
                    "message": "Hello, Matrix!",
                    "sender": "test_sender"
                })
            }).encode()
        )

        # Allow async tasks to run
        await asyncio.sleep(1)

        # Validate the mock gateway received the correct request
        assert len(gateway.received_requests) == 1
        request_data = gateway.received_requests[0]
        assert request_data["url"].endswith("/messages/send")
        assert request_data["data"]["room_id"] == "test_room"
        assert request_data["data"]["message"] == "Hello, Matrix!"
        assert request_data["data"]["sender"] == "test_sender"