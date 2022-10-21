from datetime import datetime

from apps.commons.core import BrokerAuthBearer
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, route

from ..services import exceptions, services
from . import schemas


@api_controller("/brokers", tags=["Brokers"], auth=BrokerAuthBearer())
class BrokerAPIController:
    @route.post("/cert02", url_name="Add broker detail", response={204: None})
    def add_broker_detail(self, request, info: schemas.BrokerDetailInSchema):
        try:
            services.update_broker_detail(request.auth, **info.__dict__)
        except exceptions.BrokerDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="This user is not registered."
            )
        return

    @route.post("/cert02/upload", url_name="Add broker license image", response={204: None})
    def add_broker_license_images(
        self,
        request,
        biz_registration_pic: UploadedFile = File(...),
        license_pic: UploadedFile = File(...),
    ):
        try:
            file_date_key = datetime.now().strftime("%Y%m%d%H%M%S")
            images = [biz_registration_pic, license_pic]
            for image in images:
                services.add_broker_license_images(request.auth, image, file_date_key)
        except exceptions.BrokerDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="This user is not registered."
            )
        return
