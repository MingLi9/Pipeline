import os
import requests
from flask import Request


def login(request: Request):
    auth = request.authorization
    if not auth:
        return None, ("missing credentials, 401")

    basicAuth = (auth.username, auth.password)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login",
        auth=basicAuth,
    )

    if response.status_code == 200:
        # Extract token from JSON response
        access_token = response.json().get('access_token')
        return access_token, None
    else:
        return None, (response.text, response.status_code)


def register(request: Request):
    data = request.get_json()

    if data is None or 'username' not in data or 'password' not in data:
        return None, ('Username and password are required.', 400)

    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/register",
        json=data
    )

    if response.status_code == 201:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def protected(request: Request):
    if "Authorization" not in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]

    if not token.startswith("Bearer "):
        token = f"Bearer {token}"  # Ensure the token starts with 'Bearer'

    response = requests.get(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/protected",
        headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)


def verify_token(token):
    """Verify the JWT token by calling the auth-service."""
    headers = {
        "Authorization": token
    }
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/verify",
        headers=headers
    )
    if response.status_code == 200:
        return response.json(), None  # Return the verified user info
    else:
        return None, ("Token verification failed", response.status_code)
