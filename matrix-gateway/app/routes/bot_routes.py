from fastapi import APIRouter
import httpx
from pydantic import BaseModel
from app.config import REDIS_URL, INSTANCE_IP
from app.clients import create_client, get_client_from_pool, start_sync
import redis
import json
from fastapi import HTTPException

router = APIRouter()

# Redis client
redis_client = redis.StrictRedis(host=REDIS_URL, port=6379, password='yourpassword', decode_responses=True)

class BotCredentials(BaseModel):
    username: str
    password: str

class RemoveBotRequest(BaseModel):
    username: str

async def creator_exists(creator_ip):
    url = f"http://{creator_ip}:8000"  # Ensure INSTANCE_IP is defined and valid
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            status_code = response.status_code
            print(f"Status code: {status_code}")
            return status_code == 200  # Return True if status code is 200, otherwise False
    except httpx.RequestError as e:
        print(f"Error while making request: {e}")
        return False  # Return False in case of any request error

def fetch_creator_ip(username):
    client_data = redis_client.get(username)
    if not client_data:
        raise HTTPException(status_code=404, detail="Client not found in Redis")

    client_data = json.loads(client_data)
    return client_data.get("instance_ip", "No IP found")

@router.post("/add")
async def add_bot(credentials: BotCredentials):
    # Check if the bot already exists in Redis
    if redis_client.exists(credentials.username):
        creator_ip = fetch_creator_ip(credentials.username)
        print(f"creator ip = {creator_ip}")
        alive = False
        if creator_ip != "No IP found":
            alive = await creator_exists(creator_ip)
        print(f"alive = {alive}")
        if alive:
            return {"message": "Bot already exists"}
        else:
            redis_client.delete(credentials.username)
    # Create and start syncing the bot
    client = await create_client(credentials.username, credentials.password)
    await start_sync(client)
    return {"message": f"Bot {credentials.username} added"}

@router.get("/")
async def list_bots():
    # List all bots stored in Redis
    bot_keys = redis_client.keys("*")
    return {"bots": bot_keys}

@router.post("/remove")
async def remove_bot(payload: RemoveBotRequest):
    username = payload.username

    # Check if the bot exists in Redis
    if not redis_client.exists(username):
        return {"message": "Bot not found"}

    # Retrieve the client from Redis and close it
    client = await get_client_from_pool(username)
    await client.close()

    # Remove the bot from Redis
    redis_client.delete(username)
    return {"message": f"Bot {username} removed"}