import httpx
from app.config import API_GATEWAY_URL

async def send_to_gateway(extension, payload):
    """
    Send a payload to the API gateway at the specified extension.

    Args:
        extension (str): The API endpoint extension (e.g., "/bots/ask_connection").
        payload (dict): The JSON payload to send.

    Returns:
        dict: The JSON response from the API gateway.

    Raises:
        httpx.RequestError: If a network error occurs.
        httpx.HTTPStatusError: If the API response indicates an HTTP error.
    """
    url = f"{API_GATEWAY_URL}{extension}"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()  # Raise for HTTP errors
        return response.json()
