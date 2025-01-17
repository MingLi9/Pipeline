from flask import Blueprint, jsonify, request
from datetime import datetime
import uuid

bots_blueprint = Blueprint('bots', __name__)

nats_client = None

def init_blueprint(client):
    global nats_client
    nats_client = client
    return bots_blueprint

def get_current_time_iso():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

@bots_blueprint.route("/ask_connection", methods=["POST"])
def ask_connection():
    try:
        print("Received request to /bots/ask_connection")
        if not nats_client or not nats_client.connected:
            print("NATS client is not connected!")
            raise RuntimeError("NATS client is not connected")

        connection_request = {
            "event_id": str(uuid.uuid4()),
            "timestamp": get_current_time_iso(),
            "platform": "Matrix",
            "service": "update",
            "event_type": "post",
            "actor": "Matrix-Gateway",
            "payload": "A new Matrix-Gateway service is running"
        }

        # Serialize and encode the connection request
        nats_client.publish("bots.connection", str(connection_request))

        print("Message published to NATS successfully")
        return jsonify({"message": "Bot connection request sent"}), 200
    except Exception as e:
        print(f"Error in /ask_connection: {e}")
        return jsonify({"error": str(e)}), 500

@bots_blueprint.route("/chat_message", methods=["POST"])
def chat_message():
    try:
        payload = request.json
        required_fields = ["room_id", "room_name", "sender", "receiver", "message", "timestamp"]

        # Validate the payload
        if not all(field in payload for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        print(f"Received chat message: {payload}")

        if not nats_client or not nats_client.connected:
            raise RuntimeError("NATS client is not connected")

        nats_client.publish("chat.messages", str(payload))  # Convert payload to a string for NATS
        print("Chat message published to NATS successfully")
        return jsonify({"message": "Chat message sent successfully"}), 200
    except Exception as e:
        print(f"Error in /chat_message: {e}")
        return jsonify({"error": str(e)}), 500
