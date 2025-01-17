import requests
import os


def verify_token(token):
    """Verify the JWT token by calling the auth-service."""
    headers = {
        "Authorization": token
    }

    auth_service_url = os.environ.get('AUTH_SVC_ADDRESS')
    if not auth_service_url.startswith("http"):
        auth_service_url = f"http://{auth_service_url}"

    response = requests.post(f"{auth_service_url}/verify", headers=headers)
    if response.status_code == 200:
        return True
    else:
        raise Exception("Token verification failed")
