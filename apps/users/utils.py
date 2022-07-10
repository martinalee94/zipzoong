import os

import jwt


def create_user_token(user_id, device):
    key = os.getenv("SECRET_KEY")
    encoded = jwt.encode({"user_id": user_id, "device": device}, key, algorithm="HS256")
    return encoded


def decode_user_token(token):
    key = os.getenv("SECRET_KEY")
    decoded = jwt.decode(token, key, algorithms="HS256")
    return decoded


def get_seller_from_header(request):
    token = request.headers.get("Authorization").split()[1]
    decoded_token = decode_user_token(token)
    return decoded_token
