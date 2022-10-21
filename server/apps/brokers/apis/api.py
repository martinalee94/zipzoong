from apps.commons.core import BrokerAuthBearer
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
from ninja_extra import api_controller, route

from ..services import exceptions, services
from . import schemas


@api_controller("/brokers", tags=["Brokers"], auth=BrokerAuthBearer())
class BrokerAPIController:
    @route.post("/cert02", url_name="Add broker detail", deprecated=True)
    def add_broker_detail(self, info: schemas.BrokerSignUpSchema):
        return
