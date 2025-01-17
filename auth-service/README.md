# Authentication Service

## Description

A simple authentication service to get started with the project. This service allows users to register, log in, and access a protected route using a token.

## Features

- User registration
- User login
- Access to a protected route with token authentication

## Technologies Used

- Python
- Flask
- PostgreSQL
- SQLAlchemy

## Installation Instructions

To set up the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/fuas-dverse/group.git
   cd auth-service
   ```

2. Create a `.env` file based on the provided template.

## Usage

The following endpoints are available:

- **POST /register**: Register a new user.
- **POST /login**: Log in an existing user.
- **GET /protected**: Access a protected route (requires authentication token).

---

### 1. Register a New User

**Endpoint:** `POST /register`

**Example `curl` command:**

```bash
curl -X POST http://localhost:5000/register \
-H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}'
```

### 2. Log In an Existing User

**Endpoint:** `POST /login`

**Example `curl` command:**

```bash
curl -u "your_username:your_password" \
-X POST http://localhost:5000/login
```

### 3. Access a Protected Route

**Endpoint:** `GET /protected`

You will need to include the token received from the login response in the Authorization header.

**Example `curl` command:**

```bash
curl -X GET http://localhost:5000/protected \
-H "Authorization: Bearer your_token"
```

---

## Running the Application

Use the provided script to run the application and set up the database:

```bash
./run.sh
```

## Contributing

If you'd like to contribute to this project, please submit a pull request or open an issue for discussion.
Make sure to update `requirements.txt` and `.env.template`
