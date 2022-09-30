from apps.commons.exceptions import APIException
from ninja.responses import Response
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="Zipzoong(중개의뢰인)",
    description="Zipzoong 중개의뢰인 API 문서",
    version="0.01",
)


@api.exception_handler(APIException)
@api.exception_handler(Exception)
def custom_api_exception_handler(req, exc):
    return Response(exc.__dict__)
