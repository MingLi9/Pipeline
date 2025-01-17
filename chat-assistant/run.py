import asyncio
from nats.aio.client import Client as NATS
from aiohttp import web
import json
from datetime import datetime, timezone
# from topic_finder import find_topic, clean_input_text, handle_short_inputs, refine_with_pipeline
import uuid
from dotenv import load_dotenv
import os

load_dotenv()
nc = NATS()

def get_current_time_iso():
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

async def send_credentials():
    """
    A method that executes the specific task when the payload matches.
    """
    print("Executing send_credentials...")
    credentials = {
        "username": os.getenv("BOT_USERNAME"),
        "password": os.getenv("BOT_PASSWORD"),
    }
    credentials_response = {
        "event_id": str(uuid.uuid4()),
        "timestamp": get_current_time_iso(),
        "platform": "Matrix",
        "service": "matrix-login",
        "event_type": "post",
        "actor": "Chat Assistance",
        "payload": str(credentials)
    }
    print("\n\n\n",credentials_response,"\n\n\n")
    await nc.publish("send.matrix.message", json.dumps(credentials_response).encode())
    
async def handle_specific_message(data):
    """
    Handle the message if it matches the specific payload condition.
    """
    # Check for specific payload content
    payload = data.get("payload", "")
    if payload == "A new Matrix-Gateway service is running":
        await send_credentials()
        return True  # Indicates that the message has been handled
    return False  # Indicates the message is not handled here

async def handle_normal_message(data, subject):
    """
    Handle the general messages.
    """
    receiver = data.get("receiver", "")
    username = receiver.lstrip("@").split(":")[0] if receiver else "unknown"
    room_id = data.get("room_id", "unknown_room")
    original_message = data.get("message", "no_message")

    response_message = original_message

    # # # Call the find_topic function from topic_finder.py
    # # response_message = find_topic(original_message)

    # # Step 1: Clean the input text
    # cleaned_text = clean_input_text(original_message)
    
    # # Step 2: Handle short or vague inputs
    # processed_text = handle_short_inputs(cleaned_text)
    # if "too short" in processed_text:  # Early return for short inputs
    #     response_message = processed_text
    # else:
    #     # Step 3: Refine the input using the pipeline
    #     response_message = refine_with_pipeline(processed_text)

    # # Avoid echoing the input
    # if response_message.strip().lower() == original_message.strip().lower():
    #     response_message = "I'm not sure how to respond. Can you clarify?"


    # Prepare the response object
    payload_response = {
        "username": username,
        "room_id": room_id,
        "message": response_message
    }
    message_response = {
        "event_id": str(uuid.uuid4()),
        "timestamp": get_current_time_iso(),
        "platform": "Matrix",
        "service": "matrix-message",
        "event_type": "post",
        "actor": "Chat Assistance",
        "payload": json.dumps(payload_response)
    }

    # Publish response to "send.matrix.message"
    await nc.publish("send.matrix.message", json.dumps(message_response).encode())

async def message_handler(msg):
    subject = msg.subject
    raw_data = msg.data.decode()

    try:
        # Attempt to parse the incoming message as JSON
        if raw_data.startswith("{") and raw_data.endswith("}"):
            fixed_data = raw_data.replace("'", '"')
            data = json.loads(fixed_data)
        else:
            raise ValueError(f"Received non-JSON formatted data: {raw_data}")

        print(f"Received a valid JSON message on '{subject}': {data}")

        # First, handle specific messages
        if await handle_specific_message(data):
            print("Specific message handled.")
            return

        # Otherwise, handle normal messages
        await handle_normal_message(data, subject)

    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: Invalid JSON received on '{subject}': {raw_data}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def run():
    # Initialize the NATS client

    # Connect to the NATS server
    nats_url = os.getenv("NATS_SERVER_URL")
    await nc.connect(nats_url)  # Update with your NATS server address if needed

    # Subscribe to topics
    await nc.subscribe("bots.connection", cb=message_handler)
    await nc.subscribe("chat.messages", cb=message_handler)

    print("Chat bot is listening on 'bots.connection' and 'chat.messages'...")

    try:
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down bot...")
        await nc.drain()

async def health_check(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/health", health_check)

async def main():
    await asyncio.gather(run(), web._run_app(app, port=8090))

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())