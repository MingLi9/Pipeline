from flask import Blueprint, request, jsonify
from utils import verify_token
from services import delete_user_profile, get_user_profile, update_user_profile

user_routes = Blueprint('user_routes', __name__)


# Get user profile (protected route)
@user_routes.route('/user/<int:user_id>', methods=['GET'])
def get_profile(user_id):

    token = request.headers.get("Authorization", None)
    if token:
        try:
            verify_token(token)  # Call to auth-service for token verification
        except Exception as e:
            return jsonify({"msg": str(e)}), 401

        user_profile = get_user_profile(user_id)
        if user_profile:
            return jsonify(user_profile), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify({"msg": "Missing Authorization Header"}), 401


# Update user profile (protected route)
@user_routes.route('/user/<int:user_id>', methods=['PUT'])
def update_profile(user_id):

    token = request.headers.get("Authorization", None)
    if token:
        try:
            verify_token(token)  # Call to auth-service for token verification
        except Exception as e:
            return jsonify({"msg": str(e)}), 401

        data = request.get_json()  # The updated data sent in the request body
        if not data:
            return jsonify({"msg": "No data provided"}), 400

        update_profile = update_user_profile(user_id, data)
        if update_profile:
            return jsonify(update_profile), 200

    else:
        return jsonify({"msg": "Missing Authorization Header"}), 401


# Delete a user (protected route)
@user_routes.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):

    token = request.headers.get("Authorization", None)
    if token:
        try:
            verify_token(token)  # Call to auth-service for token verification
        except Exception as e:
            return jsonify({"msg": str(e)}), 401

        # Call the delete_user function to remove the user
        user = delete_user_profile(user_id)

        # Check if the user was found and deleted
        if user:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"msg": "Missing Authorization Header"}), 401
