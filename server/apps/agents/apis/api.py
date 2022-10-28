from datetime import datetime

from apps.commons.core import AgentAuthBearer
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
from apps.houses.apis import schemas as house_schemas
from ninja import File, Query
from ninja.files import UploadedFile
from ninja_extra import api_controller, route

from ..services import exceptions, services
from . import schemas


@api_controller("/agents", tags=["Agents"], auth=AgentAuthBearer())
class AgentAPIController:
    @route.post("/cert02", url_name="Add Agent detail", response={204: None})
    def add_agent_detail(self, request, info: schemas.AgentDetailInSchema):
        try:
            services.update_agent_detail(request.auth, **info.__dict__)
        except exceptions.AgentDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="This user is not registered."
            )
        return

    @route.post("/cert02/upload", url_name="Add agent license image", response={204: None})
    def add_agent_license_images(
        self,
        request,
        biz_registration_pic: UploadedFile = File(...),
        license_pic: UploadedFile = File(...),
    ):
        try:
            file_date_key = datetime.now().strftime("%Y%m%d%H%M%S")
            images = [biz_registration_pic, license_pic]
            for image in images:
                services.add_agent_license_images(request.auth, image, file_date_key)
        except exceptions.AgentDoesNotExist:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST, message="This user is not registered."
            )
        return

    @route.get("/houses/list")
    def get_nearby_house_list(
        self, request, location, pagination: house_schemas.PaginationListSchema = Query(...)
    ):
        house_list = services.get_nearby_houses_list(
            decoded_token=request.auth,
            location=location,
            pagination=pagination,
        )

        return [
            schemas.AgentHouseListOut(page_num=pagination.page_num, num=i, house_info=house_list[i])
            for i in range(len(house_list))
        ]
