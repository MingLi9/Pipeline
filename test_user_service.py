import requests
import json

BASE_URL = "http://localhost:8080"  # API Gateway URL

# Test credentials
USERNAME = "testuse2r6334d3333"
PASSWORD = "testpassword1"
ID = 1


def register_user():
    """Register a user through the API gateway."""
    print("Registering a new user...")
    register_url = f"{BASE_URL}/api/v1/register"
    data = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = requests.post(register_url, json=data)

    # Check if the response contains JSON
    if response.headers.get("Content-Type") == "application/json":
        try:
            response_json = response.json()
            print(
                f"User {USERNAME} registered successfully with response: "
                f"{response_json}."
            )
            return response_json  # Return the user_id for later use
        except ValueError:
            print("Failed to parse JSON response")
    else:
        print(
            f"Unexpected content type: {response.headers.get('Content-Type')}"
        )

    print(f"Failed to register user: {response.status_code} {response.text}")
    return None


def login_user():
    """Log in through the API gateway and return the JWT token."""
    print("Logging in to get JWT token...")
    login_url = f"{BASE_URL}/api/v1/login"
    response = requests.post(login_url, auth=(USERNAME, PASSWORD))
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Login successful. JWT token: {token}")
        return token
    else:
        print(f"Login failed: {response.status_code} {response.text}")
        return None


def get_user_profile(user_id, token):
    """Get user profile using the JWT token."""
    print(f"Fetching user profile for user ID: {user_id}")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        f"{BASE_URL}/api/v1/user/{user_id}", headers=headers
    )
    if response.status_code == 200:
        print(f"User profile: {json.dumps(response.json(), indent=4)}")
    else:
        print(
            f"Failed to fetch user profile: {response.status_code} "
            f"{response.text}"
        )
    return response


def update_user_profile(user_id, token, data):
    """Update user profile using the JWT token."""
    print(f"Updating user profile for user ID: {user_id}")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.put(
        f"{BASE_URL}/api/v1/user/{user_id}", headers=headers, json=data
    )
    if response.status_code == 200:
        print(
            "User profile updated: "
            f"{json.dumps(response.json(), indent=4)}"
        )
    else:
        print(
            f"Failed to update user profile: {response.status_code} "
            f"{response.text}"
        )
    return response


def delete_user_profile(user_id, token):
    """Delete user profile using the JWT token."""
    print(f"Deleting user profile for user ID: {user_id}")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.delete(
        f"{BASE_URL}/api/v1/user/{user_id}", headers=headers
    )

    if response.status_code == 200:
        print(
            "User profile deleted successfully"
        )
    else:
        print(
            f"Failed to delete user profile: {response.status_code} "
            f"{response.text}"
        )

    return response


if __name__ == "__main__":
    print("Starting test script...")

    # Step 1: Register the user
    register_response = register_user()

    # Step 2: Log in to get the JWT token
    token = login_user()

    if token:
        # Step 3: Get the user profile (using the user ID 1 as an example)
        get_user_profile(user_id=ID, token=token)

        # Step 4: Update the user profile (example data to update)
        new_profile_data = {
            "username": "updateduser",
            "first_name": "new name",
            "age": 30
        }
        update_user_profile(user_id=ID, token=token, data=new_profile_data)

        # Step 5: Delete the user profile
        delete_user_profile(user_id=ID, token=token)
    else:
        print("Unable to continue tests as login failed.")
