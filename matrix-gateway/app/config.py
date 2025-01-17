from dotenv import load_dotenv
import os

load_dotenv()

HOMESERVER_URL = os.getenv("HOMESERVER_URL")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
REDIS_URL = os.getenv("REDIS_URL")
INSTANCE_IP = os.getenv("INSTANCE_IP", "unknown-instance")