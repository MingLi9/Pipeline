from flask import jsonify
from crud import get_user_by_id, update_user, delete_user
from database import get_db


def get_user_profile(user_id):
    db = next(get_db())
    try:
        user = get_user_by_id(db, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        else:
            return {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
            }

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_user_profile(user_id, data):
    db = next(get_db())
    user = get_user_by_id(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        updated_user = update_user(db, user, **data)
        return {
            "id": updated_user.id,
            "username": updated_user.username,
            "first_name": updated_user.first_name,
            "last_name": updated_user.last_name,
            "age": updated_user.age,
            "email": updated_user.email,
        }

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_user_profile(user_id):
    db = next(get_db())
    user = get_user_by_id(db, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        user = delete_user(db, user_id)
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
            }

    except Exception as e:
        return jsonify({"error": str(e)}), 500
