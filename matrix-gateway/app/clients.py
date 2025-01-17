from app.config import HOMESERVER_URL, REDIS_URL, INSTANCE_IP
from nio import AsyncClient, LoginError, InviteEvent, RoomMessageText, MatrixRoom
from fastapi import HTTPException
from .utils.event_callbacks import message_listener
import asyncio
import redis
import json
import os

# Redis client
redis_client = redis.StrictRedis(host=REDIS_URL, port=6379, password='yourpassword', decode_responses=True)

async def create_client(username: str, password: str):
    """Create and login a Matrix client."""
    print("Enter create_client()")
    client = AsyncClient(HOMESERVER_URL, username)
    print("Client created")
    try:
        response = await client.login(password)
        if not response.access_token:
            raise LoginError("Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    print("Client logged in")
    # Add client to pool
    user_id = client.user_id  # Original user_id
    username = user_id[1:].split(":")[0]
    client_data = {
        "user_id": user_id,
        "device_id": client.device_id,
        "access_token": client.access_token,
        "homeserver": HOMESERVER_URL,
        "instance_ip": INSTANCE_IP
    }
    redis_client.set(username, json.dumps(client_data))
    print("Client stored in redis")

    # Register callbacks
    print(f"Registering invite event callback for user: {client.user_id}")
    client.add_event_callback(on_invite_event, InviteEvent)
    
    # Register the message listener callback
    print(f"Registering message listener for user: {client.user_id}")
    client.add_event_callback(message_listener, RoomMessageText)
    print("Client creation finished!")

    return client

async def get_client_from_pool(user_id: str) -> AsyncClient:
    """Retrieve a client from Redis and recreate the AsyncClient."""
    client_data = redis_client.get(user_id)
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found in Redis")

    client_data = json.loads(client_data)
    client = AsyncClient(client_data["homeserver"], client_data["user_id"])
    client.access_token = client_data["access_token"]
    client.device_id = client_data["device_id"]
    return client

async def start_sync(client: AsyncClient):
    """Start syncing for a Matrix client."""
    print(f"Starting sync for user: {client.user_id}")
    try:
        # Start syncing
        asyncio.create_task(client.sync_forever(timeout=30000))
        print(f"Sync started successfully for user: {client.user_id}.")
        await asyncio.sleep(2)

        # Initial processing of pending invites
        await process_pending_invites(client)
    except Exception as e:
        print(f"Error during sync for user {client.user_id}: {e}")

async def process_pending_invites(client: AsyncClient):
    """Process pending room invites."""
    if not client.invited_rooms:
        print("No pending invites in invited_rooms.")
        return

    for room_id, room in client.invited_rooms.items():
        print(f"Processing pending invite for room: {room_id}")
        await join_room(client, room_id)

async def join_room(client: AsyncClient, room_id: str):
    """Helper function to join a room."""
    try:
        response = await client.join(room_id)
        print(f"Successfully joined room {room_id}: {response}")
    except Exception as e:
        print(f"Failed to join room {room_id}: {e}")

async def on_invite_event(event: InviteEvent, client: AsyncClient):
    """Handle new room invites dynamically."""
    try:
        # Extract room_id and own_user_id from the event
        room_id = event.room_id
        user_id = event.own_user_id

        print(f"Received an invite to room: {room_id} for user: {user_id}")

        # Fetch the client from Redis
        target_client = await get_client_from_pool(user_id)
        if target_client is None:
            print(f"No client found in pool for user: {user_id}")
            return

        print(f"Joining room {room_id} with user {user_id}")
        response = await target_client.join(room_id)
        print(f"Successfully joined room {room_id}: {response}")
    except Exception as e:
        print(f"Error processing invite event for room {room_id}: {e}")
