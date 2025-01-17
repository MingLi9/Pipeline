import asyncio
import json
from nats.aio.client import Client as NATS

async def run():
    nc = NATS()
    
    # Connect to the NATS server
    await nc.connect("nats://localhost:4222")

    # Create a JSON object
    message_data = {
        "name": "Test User",
        "age": 30,
        "email": "testuser@example.com",
        "isActive": True,
        "roles": ["user", "admin"],
        "profile": {
            "username": "testuser",
            "created_at": "2024-11-19T10:00:00Z"
        }
    }
    
    # Convert the JSON object to a bytes string
    message_bytes = json.dumps(message_data).encode('utf-8')

    # Publish the JSON message to the 'test' subject
    await nc.publish("test", message_bytes)

    # Close the connection
    await nc.close()

if __name__ == '__main__':
    asyncio.run(run())  # Use asyncio.run() instead of get_event_loop
