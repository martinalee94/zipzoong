from apps.agents.apis import schemas as agent_schemas
from apps.agents.services import exceptions as agent_exceptions
from apps.agents.services import services as agent_services
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
from ninja_extra import api_controller, route

from ..exceptions import SellerAlreadyExist, SellerDoesNotExist
from ..services import services
from . import schemas as auth_schemas


@api_controller("/auth", tags=["Auth"])
class MyTokenAPIController:
    @route.post("/users/token", response=auth_schemas.GetTokenOutSchema, url_name="getToken")
    def get_access_token_for_seller(self, user_info: auth_schemas.GetSellerTokenInSchema):
        try:
            issued_token = services.issue_seller_access_token(user_info.id, user_info.client_secret)
        except SellerDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Client secret or id is invalid."
            )
        return issued_token

    @route.post(
        "/users/token/verify",
        response=auth_schemas.VerifyIssuedTokenOutSchema,
        url_name="verifyToken",
    )
    def verify_seller_access_token_for_seller(self, token: auth_schemas.VerifyIssuedTokenInSchema):
        result = services.verify_seller_access_token(**token.__dict__)
        return result

    @route.post("/agents/login", response=auth_schemas.GetTokenOutSchema, url_name="getToken")
    def get_access_token_for_agent(self, agent_info: auth_schemas.GetAgentTokenInSchema):
        try:
            issued_token = services.issue_agent_access_token(**agent_info.__dict__)
        except SellerDoesNotExist:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="Agent info is invalid.")
        return issued_token

    @route.post(
        "/agents/token/verify",
        response=auth_schemas.VerifyIssuedTokenOutSchema,
        url_name="verifyToken",
    )
    def verify_access_token_for_agent(self, token: auth_schemas.VerifyIssuedTokenInSchema):
        result = services.verify_agent_access_token(**token.__dict__)
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
        "/agents/sign-up",
        url_name="Sign-up agent",
        response=agent_schemas.AgentSignUpOutSchema,
    )
    def register_agent(self, info: agent_schemas.AgentSignUpSchema):
        try:
            agent_services.add_new_agent(**info.__dict__)
            response = agent_services.issue_agent_access_token(**info.__dict__)
        except agent_exceptions.PasswordCheckRequired:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST,
                message="Password and confirmed password are not matched.",
            )
        except agent_exceptions.AgentAlreadyExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="Agent account is already registered."
            )
        return response
