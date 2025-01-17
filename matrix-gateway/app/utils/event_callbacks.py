from app.config import API_GATEWAY_URL
from nio import MatrixRoom, RoomMessageText
from .gateway_com import send_to_gateway
import json
import httpx

async def message_listener(room, event):
    print(f"Event: {event}, Room: {room}")
    print(f"Event type: {type(event).__name__}, Room type: {type(room).__name__}")

    if not isinstance(event, RoomMessageText):
        print("Skipping: event is not RoomMessageText")
        return

    if not isinstance(room, MatrixRoom):
        print("Skipping: room is not MatrixRoom")
        return

    sender = event.sender
    receiver = room.own_user_id
    print(f"Sender: {sender}, Receiver: {receiver}")

    if sender == receiver:
        print("Skipping: sender and receiver are the same")
        return

    payload = {
        "room_id": room.room_id,
        "room_name": room.display_name,
        "sender": sender,
        "receiver": receiver,
        "message": event.body,
        "timestamp": event.server_timestamp,
    }
    print(f"Payload to be sent: {payload}")

    await send_to_gateway("/bots/chat_message", payload)
