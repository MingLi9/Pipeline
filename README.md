# DVerse Group Project

**Important:**  
Please make pull requests to this branch; do not push directly.

## Docker Hub Credentials
- **Username:** 466069@student.fontys.nl
- **Repository:** DverseDverse

Ensure your Docker images are pushed to our Docker registry.

docker build -t dverse/gateway:latest .
docker push dverse/gateway:latest

docker build -t dverse/chat-assistant:latest .
docker push dverse/chat-assistant:latest

docker build -t dverse/matrix-gateway:latest .
docker push dverse/matrix-gateway:latest

## Setup and Testing

### 1. Clone the repository
```bash
git clone https://github.com/fuas-dverse/group.git
cd group
```

### 2. Start the Services
Use Docker Compose to start the services:
```bash
docker-compose up --build
```

### 3. Testing the Services
Run the `test_user_service.py` script to test user registration, login, and profile update functionality:
```bash
python test_user_service.py
```

This script will:
- Register a new user
- Log in and generate a JWT token
- Fetch and update the user's profile