import os
from datetime import datetime, timedelta

import jwt


class ClientToken:
    def __init__(self, id: str, client_secret: str):
        self.id = id
        self.client_secret = client_secret

    def encode(self):
        encoded_token = jwt.encode(
            {
                "id": self.id,
                "client_secret": self.client_secret,
                "exp": datetime.now() + timedelta(days=30),
            },
            os.environ.get("SECRET_KEY"),
            algorithm="HS256",
        )
        return encoded_token

    @classmethod
    def decode(cls, encoded_token):
        try:
            decoded_token = jwt.decode(
                encoded_token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
            )
        except Exception as e:
            return False
        return decoded_token


class BrokerToken:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def encode(self):
        encoded_token = jwt.encode(
            {
                "email": self.email,
                "password": self.password,
                "exp": datetime.now() + timedelta(days=1),
            },
            os.environ.get("SECRET_KEY"),
            algorithm="HS256",
        )
        return encoded_token

    @classmethod
    def decode(cls, encoded_token):
        try:
            decoded_token = jwt.decode(
                encoded_token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
            )
        except Exception as e:
            return False
        return decoded_token
