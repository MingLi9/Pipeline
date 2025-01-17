import os
from dotenv import load_dotenv
import asyncio
import json
import aiohttp
from nats.aio.client import Client as NATS

load_dotenv()
matrix_gateway_url = os.getenv("MATRIX_GATEWAY_URL")

class NATSClient:
    def __init__(self):
        self.nc = NATS()
        self.loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(self.loop)
        self.connected = False

    def connect(self, servers=["nats://localhost:4222"], ping_interval=20, max_outstanding_pings=3):
        if not self.connected:
            try:
                print(f"Connecting to NATS servers: {servers}")
                self.loop.run_until_complete(
                    self.nc.connect(
                        servers=servers,
                        ping_interval=ping_interval,
                        max_outstanding_pings=max_outstanding_pings
                    )
                )
                self.connected = True
                print("Successfully connected to NATS.")
            except Exception as e:
                print(f"Error connecting to NATS: {e}")
                raise RuntimeError(f"Failed to connect to NATS: {e}")

    def publish(self, subject, payload):
        if not self.connected:
            raise RuntimeError("NATS client is not connected")
        print(f"Publishing to subject '{subject}': {payload}")
        try:
            asyncio.run_coroutine_threadsafe(self.nc.publish(subject, payload.encode()), self.loop)
            print(f"Message published to '{subject}' successfully.")
        except Exception as e:
            print(f"Error publishing to NATS: {e}")
            raise RuntimeError(f"Failed to publish message to '{subject}': {e}")

    def subscribe(self, subject, callback):
        if not self.connected:
            raise RuntimeError("NATS client is not connected")
        print(f"Subscribing to subject: {subject}")
        asyncio.run_coroutine_threadsafe(self.nc.subscribe(subject, cb=callback), self.loop)
        
    def start_event_loop(self):
        try:
            print("Starting NATS event loop...")
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("Stopping NATS event loop...")
            self.loop.stop()

    def close(self):
        if self.connected:
            print("Closing NATS connection...")
            asyncio.run_coroutine_threadsafe(self.nc.close(), self.loop)
            self.connected = False
            print("NATS connection closed.")

# Define a callback function for the subscription
async def message_handler(msg):
    print("\n\n\nA message received\n\n\n")
    try:
        # Decode and parse the message as JSON
        data = json.loads(msg.data.decode())
        print(f"Received message on subject '{msg.subject}': {data}")

        # Route message based on 'service' field
        service = data.get("service")
        if service == "matrix-login":
            await handle_matrix_login(data)
        elif service == "matrix-message":
            await send_matrix_message(data)
        else:
            print(f"Unhandled service type: {service}")

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: Failed to decode message on '{msg.subject}': {msg.data.decode()}")
    except Exception as e:
        print(f"Unexpected error in message_handler: {e}")

async def handle_matrix_login(data):
    print("Handling 'matrix-login' service...")
    try:
        # Extract the payload from the message
        payload = data.get("payload", {})
        if isinstance(payload, str):
            # Replace single quotes with double quotes to make it JSON-compliant
            payload = payload.replace("'", '"')
            payload = json.loads(payload)
        
        # Extract username and password from the payload
        username = payload.get("username")
        password = payload.get("password")

        if username and password:
            print(f"Extracted credentials - Username: {username}, Password: {password}")
            # Prepare the API request data
            api_payload = {
                "username": username,
                "password": password
            }

            # Use the reusable API request function
            url = f"{matrix_gateway_url}/bots/add"
            # url = "http://localhost:8000/bots/add"
            await send_api_request(url, api_payload)
        else:
            print("Invalid payload: Missing username or password.")

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError while parsing payload: {data.get('payload')}")
    except Exception as e:
        print(f"Unexpected error in handle_matrix_login: {e}")


async def send_api_request(url, payload, headers=None):
    """
    A reusable function to send an API request.
    
    Args:
        url (str): The API endpoint URL.
        payload (dict): The JSON payload to send in the request.
        headers (dict): The HTTP headers to include in the request.
    
    Returns:
        None
    """
    if headers is None:
        headers = {"Content-Type": "application/json"}
    
    async with aiohttp.ClientSession() as session:
        try:
            print(f"Sending API request to {url} with payload: {payload}")
            response = await session.post(url, json=payload, headers=headers)
            if response.status == 200:
                print(f"Request to {url} successful.")
            else:
                print(f"Failed to send request to {url}: {response.status} - {await response.text()}")
        except Exception as e:
            print(f"Error sending request to {url}: {e}")

async def send_matrix_message(data):
    print("Handling 'matrix-message' service...")
    try:
        # Extract the payload from the message
        payload = data.get("payload", {})
        if isinstance(payload, str):
            # Replace single quotes with double quotes to make it JSON-compliant
            payload = payload.replace("'", '"')
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError as e:
                print(f"Error parsing payload: {payload}")
                raise e

        # Send the payload to the API endpoint
        url = f"{matrix_gateway_url}/messages/send"
        # url = "http://localhost:8000/messages/send"
        await send_api_request(url, payload)

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError while parsing payload: {data.get('payload')} - Error: {e}")
    except Exception as e:
        print(f"Unexpected error in send_matrix_message: {e}")
