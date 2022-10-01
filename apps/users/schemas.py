from ninja_schema import ModelSchema, Schema

from .models import Seller


class GetTokenInSchema(ModelSchema):
    class Config:
        model = Seller
        include = ["id", "client_secret"]


class GetTokenOutSchema(Schema):
    access: str


class VerifyIssuedTokenInSchema(Schema):
    token: str


class VerifyIssuedTokenOutSchema(Schema):
    token_state: str


class CreateSellerServerIdOutSchema(Schema):
    id: str


class CreateSellerServerIdInSchema(Schema):
    client_secret: str
