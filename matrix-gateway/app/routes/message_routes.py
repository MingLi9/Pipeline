from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import REDIS_URL
from app.clients import get_client_from_pool
import redis

router = APIRouter()

# Redis client
redis_client = redis.StrictRedis(host=REDIS_URL, port=6379, password='yourpassword', decode_responses=True)

# Define a request model
class MessageRequest(BaseModel):
    username: str
    room_id: str
    message: str

@router.post("/send")
async def send_message(payload: MessageRequest):
    username = payload.username
    room_id = payload.room_id
    message = payload.message

    # Check if the bot exists in Redis
    if not redis_client.exists(username):
        raise HTTPException(status_code=404, detail="Bot not found")

    # Retrieve the bot's client and send the message
    try:
        client = await get_client_from_pool(username)
        await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={"msgtype": "m.text", "body": message},
        )
        return {"message": f"Message sent to {room_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {e}")