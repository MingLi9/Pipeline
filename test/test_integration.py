import pytest
import asyncio
import requests
import json
from nats.aio.client import Client as NATS

from dotenv import load_dotenv
import os

load_dotenv()

API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
NATS_SERVER_URL = os.getenv("NATS_SERVER_URL")

@pytest.mark.asyncio
async def test_bots_connection_gateway_to_nats():
    """Basic integration test to check API response and NATS message."""
    nc = NATS()
    await nc.connect(servers=[NATS_SERVER_URL])

    topic = "bots.connection"
    messages = []

    async def message_handler(msg):
        messages.append(msg.data.decode())

    await nc.subscribe(topic, cb=message_handler)
    await nc.flush()  # Ensure subscription is active

    response = requests.post(f"{API_GATEWAY_URL}/bots/ask_connection")
    assert response.status_code == 200
    assert response.json() == {"message": "Bot connection request sent"}

    await asyncio.sleep(1)

    assert len(messages) == 1
    message_data = eval(messages[0])
    
    assert message_data["platform"] == "Matrix"
    assert message_data["event_type"] == "post"
    assert "timestamp" in message_data

    await nc.drain()
    await nc.close()

@pytest.mark.asyncio
async def test_bots_chat_massage_gateway_to_nats():
    """Test to check the /bots/chat_message endpoint and NATS integration."""
    nc = NATS()
    await nc.connect(servers=[NATS_SERVER_URL])

    topic = "chat.messages"
    messages = []

    async def message_handler(msg):
        messages.append(msg.data.decode())

    await nc.subscribe(topic, cb=message_handler)
    await nc.flush()  # Ensure subscription is active

    payload = {
        "room_id": "12345",
        "room_name": "Test Room",
        "sender": "user1",
        "receiver": "user2",
        "message": "Hello, this is a test message!",
        "timestamp": "2025-01-12T12:00:00Z"
    }

    response = requests.post(f"{API_GATEWAY_URL}/bots/chat_message", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Chat message sent successfully"}

    await asyncio.sleep(1)

    assert len(messages) == 1
    received_payload = eval(messages[0])

    assert received_payload["room_id"] == payload["room_id"]
    assert received_payload["room_name"] == payload["room_name"]
    assert received_payload["sender"] == payload["sender"]
    assert received_payload["receiver"] == payload["receiver"]
    assert received_payload["message"] == payload["message"]
    assert received_payload["timestamp"] == payload["timestamp"]

    await nc.drain()
    await nc.close()

@pytest.mark.asyncio
async def test_chat_bot_to_nats_login():
    """Test to check the chatbot integration with NATS."""
    nc = NATS()
    await nc.connect(servers=[NATS_SERVER_URL])

    messages = []

    async def message_handler(msg):
        messages.append(msg.data.decode())

    await nc.subscribe("send.matrix.message", cb=message_handler)
    await nc.flush()  # Ensure subscription is active

    test_message = {
        "payload": "A new Matrix-Gateway service is running",
        "other_data": "Some additional data"
    }
    await nc.publish("bots.connection", json.dumps(test_message).encode())

    await asyncio.sleep(2)

    assert len(messages) == 1
    response_message = json.loads(messages[0])

    assert response_message["event_type"] == "post"
    assert response_message["service"] == "matrix-login"
    assert "timestamp" in response_message
    assert "event_id" in response_message
    assert "payload" in response_message

    await nc.drain()
    await nc.close()

@pytest.mark.asyncio
async def test_chat_bot_to_nats_message():
    """Test to check the chatbot integration with NATS."""
    nc = NATS()
    await nc.connect(servers=[NATS_SERVER_URL])

    messages = []

    async def message_handler(msg):
        messages.append(msg.data.decode())

    await nc.subscribe("send.matrix.message", cb=message_handler)
    await nc.flush()  # Ensure subscription is active

    test_message = {
        'room_id': '12345',
        'room_name': 'Test Room',
        'sender': 'user1',
        'receiver': 'user2',
        'message': 'Hello, this is a test message!',
        'timestamp': '2025-01-12T12:00:00Z'}
    await nc.publish("chat.messages", json.dumps(test_message).encode())

    await asyncio.sleep(2)

    assert len(messages) == 1
    response_message = json.loads(messages[0])

    assert response_message["event_type"] == "post"
    assert response_message["service"] == "matrix-message"
    assert "timestamp" in response_message
    assert "event_id" in response_message
    assert "payload" in response_message

    await nc.drain()
    await nc.close()

@pytest.mark.asyncio
async def test_full_flow_login():
    """integration test to check the login flow."""
    nc = NATS()
    await nc.connect(servers=[NATS_SERVER_URL])

    messages = []
    messages_return = []

    async def message_handler(msg):
        messages.append(msg.data.decode())
    
    async def message_handler_return(msg):
        messages_return.append(msg.data.decode())

    await nc.subscribe("bots.connection", cb=message_handler)
    await nc.subscribe("send.matrix.message", cb=message_handler_return)
    await nc.flush()  # Ensure subscription is active

    response = requests.post(f"{API_GATEWAY_URL}/bots/ask_connection")
    assert response.status_code == 200
    assert response.json() == {"message": "Bot connection request sent"}

    # wait for initial message to be sent on nats
    await asyncio.sleep(1)

    assert len(messages) == 1
    message_data = eval(messages[0])
    
    assert message_data["platform"] == "Matrix"
    assert message_data["event_type"] == "post"
    assert "timestamp" in message_data

    # wait for response message to be sent on nats
    await asyncio.sleep(5)

    assert len(messages_return) == 1
    response_message = json.loads(messages_return[0])

    assert response_message["event_type"] == "post"
    assert response_message["service"] == "matrix-login"
    assert "timestamp" in response_message
    assert "event_id" in response_message
    assert "payload" in response_message

    await nc.drain()
    await nc.close()

@pytest.mark.asyncio
async def test_full_flow_message():
    """integration test to check the incomming matrix-message flow."""
    nc = NATS()
    await nc.connect(servers=[NATS_SERVER_URL])

    messages = []
    messages_return = []

    async def message_handler(msg):
        messages.append(msg.data.decode())
    
    async def message_handler_return(msg):
        messages_return.append(msg.data.decode())

    await nc.subscribe("chat.messages", cb=message_handler)
    await nc.subscribe("send.matrix.message", cb=message_handler_return)
    await nc.flush()  # Ensure subscription is active

    payload = {
        "room_id": "12345",
        "room_name": "Test Room",
        "sender": "user1",
        "receiver": "user2",
        "message": "Hello, this is a test message!",
        "timestamp": "2025-01-12T12:00:00Z"
    }

    response = requests.post(f"{API_GATEWAY_URL}/bots/chat_message", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Chat message sent successfully"}

    # wait for initial message to be sent on nats
    await asyncio.sleep(1)

    assert len(messages) == 1
    message_data = eval(messages[0])
    
    assert message_data["room_id"] == payload["room_id"]
    assert message_data["room_name"] == payload["room_name"]
    assert message_data["sender"] == payload["sender"]
    assert message_data["receiver"] == payload["receiver"]
    assert message_data["message"] == payload["message"]
    assert message_data["timestamp"] == payload["timestamp"]

    # wait for response message to be sent on nats
    await asyncio.sleep(5)

    assert len(messages_return) == 1
    response_message = json.loads(messages_return[0])

    assert response_message["event_type"] == "post"
    assert response_message["service"] == "matrix-message"
    assert "timestamp" in response_message
    assert "event_id" in response_message
    assert "payload" in response_message

    await nc.drain()
    await nc.close()
