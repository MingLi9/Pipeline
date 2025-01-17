import os
from dotenv import load_dotenv
import threading
from flask import Flask, request, jsonify
import requests
from auth_svc import access
from marketplace_svc import marketplace
from matrix_com.matrix_com import init_blueprint
from nats_client.nats_client import NATSClient, message_handler

server = Flask(__name__)

load_dotenv()
# Get NATS server URL from environment variables
nats_server_url = os.getenv("NATS_SERVER_URL", "nats://localhost:4222")  # Default to localhost if not set

# Instantiate NATS client
nats_client = NATSClient()

server.register_blueprint(init_blueprint(nats_client), url_prefix='/bots')

def handle_error_response(error):
    if error:
        error_message, status_code = error
        return jsonify({"error": error_message}), status_code
    return None


# Login route
@server.route("/api/v1/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return jsonify({"access_token": token}), 200
    else:
        return jsonify({"error": err}), 401


# Register route
@server.route("/api/v1/register", methods=["POST"])
def register():
    success, err = access.register(request)

    if not err:
        return jsonify(success), 201
    else:
        return jsonify({"error": err}), 400


# Example of protected route
@server.route("/api/v1/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization", None)

    if not token:
        return jsonify({"error": "Missing Authorization Header"}), 401

    verified_user, err = access.verify_token(token)

    if verified_user:
        return jsonify({
            "message": "Access granted",
            "user": verified_user
        }), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401


# Forward request to user-service
@server.route("/api/v1/user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    token = request.headers.get("Authorization", None)

    if not token:
        return jsonify({"error": "Missing Authorization Header"}), 401

    # Verify token first
    verified_user, err = access.verify_token(token)

    if not verified_user:
        return jsonify({"error": "Unauthorized"}), 401

    # Forward the request to user-service
    try:
        user_service_url = f"http://user-service:5002/user/{user_id}"
        headers = {"Authorization": token}
        response = requests.get(user_service_url, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Forward request to user-service
@server.route("/api/v1/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    token = request.headers.get("Authorization", None)

    if not token:
        return jsonify({"error": "Missing Authorization Header"}), 401

    # Verify token first
    verified_user, err = access.verify_token(token)

    if not verified_user:
        return jsonify({"error": "Unauthorized"}), 401

    # Get the data to update from the request body
    update_data = request.get_json()
    if not update_data:
        return jsonify({"error": "No data provided"}), 400

    # Forward the request to user-service
    try:
        user_service_url = f"http://user-service:5002/user/{user_id}"
        headers = {"Authorization": token, "Content-Type": "application/json"}
        response = requests.put(
            user_service_url, headers=headers, json=update_data
        )

        # Return the response from the user-service
        return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Forward request to user-service
@server.route("/api/v1/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    token = request.headers.get("Authorization", None)

    if not token:
        return jsonify({"error": "Missing Authorization Header"}), 401

    # Verify token first
    verified_user, err = access.verify_token(token)

    if not verified_user:
        return jsonify({"error": "Unauthorized"}), 401

    # Forward the request to user-service
    try:
        user_service_url = f"http://user-service:5002/user/{user_id}"
        headers = {"Authorization": token}
        response = requests.delete(user_service_url, headers=headers)

        # Return the response from the user-service
        return response.json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ------- User Routes -------

@server.route("/api/v1/users/", methods=["POST"])
def add_user():
    user, error = marketplace.add_user(request)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(user), 201


@server.route("/api/v1/users/", methods=["GET"])
def get_users():
    users, error = marketplace.get_users()
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(users), 200


@server.route("/api/v1/users/<username>", methods=["GET"])
def get_user_by_username(username):
    user, error = marketplace.get_user_by_username(username)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(user), 200


@server.route("/api/v1/users/<username>", methods=["DELETE"])
def delete_user_by_username(username):
    _, error = marketplace.delete_user(username)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return '', 204


# ------- Product Routes -------

@server.route("/api/v1/products/", methods=["POST"])
def add_product():
    product, error = marketplace.add_product(request)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(product), 201


@server.route("/api/v1/products/", methods=["GET"])
def get_products():
    products, error = marketplace.get_products()
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(products), 200


@server.route("/api/v1/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product, error = marketplace.get_product_by_id(product_id)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(product), 200


@server.route("/api/v1/products/<int:product_id>/review/", methods=["POST"])
def update_product_rating(product_id):
    product, error = marketplace.update_product_rating(request, product_id)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(product), 200


@server.route("/api/v1/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    _, error = marketplace.delete_product(product_id)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return '', 204


# ------- Review Routes -------

@server.route("/api/v1/reviews/", methods=["POST"])
def add_review():
    review, error = marketplace.add_review(request)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(review), 201


@server.route("/api/v1/reviews/", methods=["GET"])
def get_reviews():
    reviews, error = marketplace.get_reviews()
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(reviews), 200


@server.route("/api/v1/reviews/<int:product_id>", methods=["GET"])
def get_reviews_per_product(product_id):
    reviews, error = marketplace.get_reviews_per_product(product_id)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(reviews), 200


# ------- Transaction Routes -------

@server.route("/api/v1/transactions/", methods=["POST"])
def add_transaction():
    transaction, error = marketplace.add_transaction(request)
    if error_response := handle_error_response(error):
        return error_response
    return jsonify(transaction), 201


@server.route("/api/v1/transactions/", methods=["GET"])
def get_all_transactions():
    transactions, error = marketplace.get_all_transactions()
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(transactions), 200


@server.route("/api/v1/transactions/<int:user_id>", methods=["GET"])
def get_user_transactions(user_id):
    transactions, error = marketplace.get_user_transactions(user_id)
    error_response = handle_error_response(error)
    if error_response:
        return error_response
    return jsonify(transactions), 200

# Function to run Flask app
def run_flask():
    print("Starting Flask API...")
    server.run(host="0.0.0.0", port=8080)

# Function to run NATS event loop
def run_nats():
    print("Starting NATS client...")
    nats_client.connect(servers=[nats_server_url])
    nats_client.subscribe("send.matrix.message", message_handler)
    nats_client.start_event_loop()

if __name__ == "__main__":
    try:
        # Start Flask in a separate thread
        flask_thread = threading.Thread(target=run_flask)
        flask_thread.daemon = True  # Ensure Flask thread exits with the main program
        flask_thread.start()

        # Run NATS in the main thread
        run_nats()
    finally:
        if nats_client.connected:
            print("Closing NATS connection...")
            nats_client.close()