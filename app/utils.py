import uuid
import json
import string
import random


def generate_uuid():
    return str(uuid.uuid4())

def generate_custom_id(length=13):
    characters = string.ascii_lowercase + string.digits  # a-z и 0-9
    return ''.join(random.choice(characters) for _ in range(length))

def create_settings_for_update_key(date, key_uuid, key_email, inbound_id=2) -> dict:
    timestamp = int(date.timestamp() * 1000)

    client_data = {
        "id": key_uuid,
        "flow": "xtls-rprx-vision",
        "email": key_email,
        "limitIp": 0,
        "totalGB": 0,
        "expiryTime": timestamp,
        "enable": True,
        "tgId": "",
        "subId": key_email,
        "reset": 0
    }

    settings_json = json.dumps({"clients": [client_data]}, separators=(',', ':'))

    return {
        "id": inbound_id,
        "settings": settings_json
    }
