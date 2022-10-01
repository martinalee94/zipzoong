import os
from datetime import datetime, timedelta

import jwt


class ClientToken:
    def __init__(self, id, client_secret):
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
            jwt.decode(encoded_token, os.environ.get("SECRET_KEY"), algorithms=["HS256"])
        except Exception as e:
            return False
        return True
