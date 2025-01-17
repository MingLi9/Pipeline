import bcrypt
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required
)
from database import get_db
from crud import (
    create_user,
    get_user_by_username,
    create_token,
    get_token,
    revoke_token
)
from database import engine
from models import Base


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "your_jwt_secret_key"
jwt = JWTManager(app)

Base.metadata.create_all(bind=engine)


# Register route
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    db = next(get_db())

    if get_user_by_username(db, data['username']):
        return jsonify({"msg": "User already exists"}), 400

    user = create_user(db, data['username'], data['password'])
    return jsonify({
        "msg": "User registered successfully",
        "user_id": user.id
    }), 201


@app.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"msg": "Missing credentials"}), 401

    db = next(get_db())
    user = get_user_by_username(db, auth.username)

    if user and bcrypt.checkpw(
        auth.password.encode('utf-8'),
        user.password.encode('utf-8')
    ):
        access_token = create_access_token(
            identity={"username": user.username, "user_id": user.id}
        )
        create_token(db, access_token, user.id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Bad username or password"}), 401


# Verify token
@app.route("/verify", methods=["POST"])
@jwt_required()
def verify_token():
    db = next(get_db())
    token_str = request.headers.get("Authorization").split(" ")[1]
    token = get_token(db, token_str)

    if not token or token.revoked:
        return jsonify({"msg": "Token invalid or revoked"}), 401

    return jsonify(get_jwt_identity()), 200


# Logout (Revoke token)
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    db = next(get_db())
    token_str = request.headers.get("Authorization").split(" ")[1]
    token = get_token(db, token_str)
    if token:
        revoke_token(db, token)
        return jsonify({"msg": "Token revoked successfully"}), 200
    return jsonify({"msg": "Token not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
