import json
from typing import Any

from apps.commons.exceptions import APIException as CustomAPIException
from apps.houses.apis.api import HouseAPIController
from apps.users.apis.api import MyTokenAPIController, UserAPIController
from django.http import HttpRequest
from ninja.renderers import JSONRenderer
from ninja.responses import Response
from ninja_extra import NinjaExtraAPI


class CustomRenderer(JSONRenderer):
    def render(self, request: HttpRequest, data: Any, *, response_status: int):
        data = {
            "respCode": response_status,
            "data": data,
        }
        return json.dumps(data, cls=self.encoder_class, **self.json_dumps_params)


api = NinjaExtraAPI(
    title="Zipzoong(중개의뢰인)",
    description="Zipzoong 중개의뢰인 API 문서",
    version="0.01",
    renderer=CustomRenderer(),
)


@api.exception_handler(CustomAPIException)
def custom_api_exception_handler(req, exc):
    exc_dict = exc.__dict__
    return Response(exc_dict, status=exc_dict["status_code"])


@api.exception_handler(Exception)
def custom_api_exception_handler(req, exc):
    return Response(str(exc), status=400)


api.register_controllers(MyTokenAPIController)
api.register_controllers(UserAPIController)
api.register_controllers(HouseAPIController)
