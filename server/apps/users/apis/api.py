from apps.brokers.apis import schemas as broker_schemas
from apps.brokers.services import exceptions as broker_exceptions
from apps.brokers.services import services as broker_services
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
from ninja_extra import api_controller, route

from ..exceptions import SellerAlreadyExist, SellerDoesNotExist
from ..services import services
from . import schemas as auth_schemas


@api_controller("/auth", tags=["Auth"])
class MyTokenAPIController:
    @route.post("/sellers/token", response=auth_schemas.GetTokenOutSchema, url_name="getToken")
    def get_access_token_for_seller(self, user_info: auth_schemas.GetSellerTokenInSchema):
        try:
            issued_token = services.issue_seller_access_token(user_info.id, user_info.client_secret)
        except SellerDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Client secret or id is invalid."
            )
        return issued_token

    @route.post(
        "/sellers/token/verify",
        response=auth_schemas.VerifyIssuedTokenOutSchema,
        url_name="verifyToken",
    )
    def verify_seller_access_token_for_seller(self, token: auth_schemas.VerifyIssuedTokenInSchema):
        result = services.verify_seller_access_token(**token.__dict__)
        return result

    @route.post("/brokers/login", response=auth_schemas.GetTokenOutSchema, url_name="getToken")
    def get_access_token_for_broker(self, broker_info: auth_schemas.GetBrokerTokenInSchema):
        try:
            issued_token = services.issue_broker_access_token(**broker_info.__dict__)
        except SellerDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Broker info is invalid."
            )
        return issued_token

    @route.post(
        "/brokers/token/verify",
        response=auth_schemas.VerifyIssuedTokenOutSchema,
        url_name="verifyToken",
    )
    def verify_access_token_for_broker(self, token: auth_schemas.VerifyIssuedTokenInSchema):
        result = services.verify_broker_access_token(**token.__dict__)
        return result


@api_controller("/users", tags=["User"])
class UserAPIController:
    @route.post(
        "/client-id", response=auth_schemas.CreateSellerServerIdOutSchema, url_name="getClientId"
    )
    def get_client_id(self, client_secret: auth_schemas.CreateSellerServerIdInSchema):
        """
        ## Body
            client_secret(클라이언트 id)\n

        ## Response
            id(서버id)
        """
        try:
            seller = services.create_server_id_for_user(**client_secret.__dict__)
            seller = auth_schemas.CreateSellerServerIdOutSchema.from_orm(seller)
        except SellerAlreadyExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Client secret already exists."
            )
        return seller

    @route.post(
        "/brokers/sign-up",
        url_name="Sign-up broker",
        response=broker_schemas.BrokerSignUpOutSchema,
    )
    def register_broker(self, info: broker_schemas.BrokerSignUpSchema):
        try:
            broker_services.add_new_broker(**info.__dict__)
            response = broker_services.issue_broker_access_token(**info.__dict__)
        except broker_exceptions.PasswordCheckRequired:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST,
                message="Password and confirmed password are not matched.",
            )
        except broker_exceptions.BrokerAlreadyExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Broker account is already registered."
            )
        return response
