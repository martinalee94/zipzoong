from apps.commons.core import AuthBearer
from ninja_extra import api_controller, route


@api_controller("/brokers", tags=["Brokers"], auth=AuthBearer())
class BrokerAPIController:
    @route.post("/sign-up")
    def register_broker(self):
        pass
