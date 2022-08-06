import os

import jwt


def create_user_token(user_id, device):
    key = os.getenv("SECRET_KEY")
    encoded = jwt.encode({"user_id": user_id, "device": device}, key, algorithm="HS256")
    print(encoded)
    return encoded


def decode_user_token(token):
    key = os.getenv("SECRET_KEY")
    decoded = jwt.decode(token, key, algorithms="HS256")
    print(decoded)
    return decoded
