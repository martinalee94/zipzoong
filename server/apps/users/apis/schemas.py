from apps.agents.domains.models import Agent
from ninja_schema import ModelSchema, Schema

from ..domains.models import Seller


class GetSellerTokenInSchema(ModelSchema):
    class Config:
        model = Seller
        include = ["id", "client_secret"]


class GetAgentTokenInSchema(ModelSchema):
    class Config:
        model = Agent
        include = ["email", "password"]


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
