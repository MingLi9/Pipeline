import os
import sys
import ast
import pytest
from flask import Flask

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from matrix_com.matrix_com import init_blueprint, bots_blueprint

class MockNATSClient:
    def __init__(self):
        self.connected = True
        self.published_messages = []
        
    def publish(self, subject, message):
        self.published_messages.append({
            'subject': subject,
            'message': message
        })

@pytest.fixture
def mock_nats():
    return MockNATSClient()

@pytest.fixture
def app(mock_nats):
    app = Flask(__name__)
    app.register_blueprint(init_blueprint(mock_nats), url_prefix='/bots')
    # Store mock_nats in app context for access in tests
    app.mock_nats = mock_nats
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_ask_connection_endpoint(client, app):
    # Make request to the endpoint
    response = client.post('/bots/ask_connection')
    
    # Check response
    assert response.status_code == 200
    assert response.json['message'] == "Bot connection request sent"
    
    # Verify NATS message using the stored mock_nats
    mock_nats = app.mock_nats
    assert len(mock_nats.published_messages) == 1
    published = mock_nats.published_messages[0]
    assert published['subject'] == 'bots.connection'
    
    # Parse the message string back to dict for verification
    message = ast.literal_eval(published['message'])  # Using eval since the message is stringified dict
    assert isinstance(message['event_id'], str)
    assert isinstance(message['timestamp'], str)
    assert message['platform'] == 'Matrix'
    assert message['service'] == 'update'
    assert message['event_type'] == 'post'
    assert message['actor'] == 'Matrix-Gateway'
    assert message['payload'] == 'A new Matrix-Gateway service is running'

def test_chat_message_endpoint_success(client, app):
    test_payload = {
        "room_id": "test_room",
        "room_name": "Test Room",
        "sender": "test_sender",
        "receiver": "test_receiver",
        "message": "Hello, world!",
        "timestamp": "2024-01-08T12:00:00Z"
    }
    
    # Make request to the endpoint
    response = client.post('/bots/chat_message', 
                         json=test_payload,
                         content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    assert response.json['message'] == "Chat message sent successfully"
    
    # Verify NATS message
    mock_nats = app.mock_nats
    assert len(mock_nats.published_messages) == 1
    published = mock_nats.published_messages[0]
    assert published['subject'] == 'chat.messages'

def test_chat_message_endpoint_missing_fields(client, app):
    incomplete_payload = {
        "room_id": "test_room",
        "sender": "test_sender"
        # Missing required fields
    }
    
    # Make request to the endpoint
    response = client.post('/bots/chat_message', 
                         json=incomplete_payload,
                         content_type='application/json')
    
    # Check response
    assert response.status_code == 400
    assert 'error' in response.json
    assert response.json['error'] == "Missing required fields"
    
    # Verify no NATS message was published
    mock_nats = app.mock_nats
    assert len(mock_nats.published_messages) == 0

def test_nats_connection_failure(app):
    # Create a new app instance with a disconnected NATS client
    mock_nats = MockNATSClient()
    mock_nats.connected = False
    
    test_app = Flask(__name__)
    test_app.register_blueprint(init_blueprint(mock_nats), url_prefix='/bots')
    test_client = test_app.test_client()
    
    # Test ask_connection endpoint
    response = test_client.post('/bots/ask_connection')
    assert response.status_code == 500
    assert 'error' in response.json
    assert "NATS client is not connected" in response.json['error']
    
    # Test chat_message endpoint
    test_payload = {
        "room_id": "test_room",
        "room_name": "Test Room",
        "sender": "test_sender",
        "receiver": "test_receiver",
        "message": "Hello, world!",
        "timestamp": "2024-01-08T12:00:00Z"
    }
    
    response = test_client.post('/bots/chat_message', 
                              json=test_payload,
                              content_type='application/json')
    assert response.status_code == 500
    assert 'error' in response.json
    assert "NATS client is not connected" in response.json['error']