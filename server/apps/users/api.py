from ninja_extra import api_controller, route

from apps.commons.exceptions import APIException, APIExceptionErrorCodes

from . import services
from .exceptions import SellerAlreadyExist, SellerDoesNotExist
from .schemas import (
    CreateSellerServerIdInSchema,
    CreateSellerServerIdOutSchema,
    GetTokenInSchema,
    GetTokenOutSchema,
    VerifyIssuedTokenInSchema,
    VerifyIssuedTokenOutSchema,
)


@api_controller("/auth", tags=["Auth"])
class MyTokenAPIController:
    @route.post("/token", response=GetTokenOutSchema, url_name="getToken")
    def get_access_token(self, user_info: GetTokenInSchema):
        try:
            issued_token = services.issue_access_token(user_info.id, user_info.client_secret)
        except SellerDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Client secret or id is invalid."
            )
        return issued_token

    @route.post("/token/verify", response=VerifyIssuedTokenOutSchema, url_name="verifyToken")
    def verify_access_token(self, token: VerifyIssuedTokenInSchema):
        result = services.verify_access_token(**token.__dict__)
        return result


@api_controller("/users", tags=["User"])
class UserAPIController:
    @route.post("/client-id", response=CreateSellerServerIdOutSchema, url_name="getClientId")
    def get_client_id(self, client_secret: CreateSellerServerIdInSchema):
        """
        ## Body
            client_secret(클라이언트 id)\n

        ## Response
            id(서버id)
        """
        try:
            seller = services.create_server_id_for_user(**client_secret.__dict__)
            seller = CreateSellerServerIdOutSchema.from_orm(seller)
        except SellerAlreadyExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Client secret already exists."
            )
        return seller
