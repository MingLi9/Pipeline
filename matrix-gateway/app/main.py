import app.utils.asyncio_patch
from fastapi import FastAPI
from app.routes import bot_routes, message_routes
from contextlib import asynccontextmanager
from app.config import API_GATEWAY_URL
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting application...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_GATEWAY_URL}/bots/ask_connection")
            if response.status_code == 200:
                print("Successfully asked bots to connect.")
            else:
                print(f"Ask bots to connect failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during startup script: {e}")

    # Yield control to the application
    yield

    # Shutdown logic
    print("Shutting down application...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_GATEWAY_URL}/bots/disconnect")
            if response.status_code == 200:
                print("Successfully send a disconnect message to all relevant bots.")
            else:
                print(f"Failed to send a disconnect message to all relevant bots: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during shutdown: {e}")


# Pass the lifespan function to FastAPI
app = FastAPI(lifespan=lifespan)

# Include API routes
app.include_router(bot_routes.router, prefix="/bots", tags=["Bots"])
app.include_router(message_routes.router, prefix="/messages", tags=["Messages"])

@app.get("/")
async def root():
    return {"message": "Matrix-Gateway Microservice is running!"}
