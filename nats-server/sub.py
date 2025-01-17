import asyncio
from nats.aio.client import Client as NATS

async def run():
    nc = NATS()

    # Connect to the NATS server
    await nc.connect("nats://localhost:4222")

    # Define a callback to handle incoming messages
    async def message_handler(msg):
        print(f"Received a message: {msg.data.decode()}")

    # Subscribe to the 'test' subject
    await nc.subscribe("test", cb=message_handler)

    # Keep the connection open to receive messages
    await asyncio.sleep(50)
    await nc.close()

if __name__ == '__main__':
    asyncio.run(run())  # Use asyncio.run() instead of get_event_loop
