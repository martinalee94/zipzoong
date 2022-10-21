from apps.commons.core import BrokerAuthBearer
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
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
