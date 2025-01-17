from flask import Flask
from routes import user_routes

app = Flask(__name__)

# Register the user routes blueprint
app.register_blueprint(user_routes)

if __name__ == "__main__":
    app.run(debug=True, port=5002, host="0.0.0.0")
