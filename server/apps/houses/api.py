from typing import List

from ninja import File
from ninja.files import UploadedFile
from ninja_extra import api_controller, route

from apps.commons.core import AuthBearer
from apps.commons.exceptions import APIException, APIExceptionErrorCodes

from . import services
from .exceptions import HouseNotFound, SellerNotFound
from .schemas import (
    CreateHouseAddressInSchema,
    CreateHouseAddressOutSchema,
    ListHouseDefaultOptionsOutSchema,
    UpdateHouseCharterPriceInSchema,
    UpdateHouseMonthlyPriceInSchema,
    UpdateHouseSalePriceInSchema,
    UpdateHouseSelectedOptionsInSchema,
)


@api_controller("/houses", tags=["Houses"], auth=AuthBearer())
class HouseAPIController:
    @route.post("/address", url_name="saveAddress", response={200: CreateHouseAddressOutSchema})
    def save_address(self, addr_info: CreateHouseAddressInSchema):
        """
        ## Body
            seller_id(의뢰인 서버쪽 id)
            sido_addr(시도 주소)
            gungu_addr(시군구 주소)
            street_addr(도로 주소)
            detail_addr(상세 주소 - default:None)
            postal_code(우편 번호 - default:None)
        """
        try:
            house = services.add_house(**addr_info.__dict__)
            house = CreateHouseAddressOutSchema.from_orm(house)
        except SellerNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="Seller id is invalid")
        return house

    @route.post("/{house_id}/mont", url_name="saveMonthlyPrice", response={204: None})
    def save_monthly_price(self, house_id: str, monthly_price: UpdateHouseMonthlyPriceInSchema):
        """
        ## Params
            house_id(매물 id)\n

        ## Body
            deposit(매물 보증금)
            monthly_rent(매물 월세가)\n
        """
        try:
            services.update_house_monthly_price(house_id, **monthly_price.__dict__)
        except HouseNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="House id is invalid")
        return 204

    @route.post("/{house_id}/char", url_name="saveCharterPrice", response={204: None})
    def save_charter_price(self, house_id: str, char_price: UpdateHouseCharterPriceInSchema):
        """
        ## Params
            house_id(매물 id)\n

        ## Body
            charter_rent(매물 전세가)\n
        """
        try:
            services.update_house_charter_price(house_id, **char_price.__dict__)
        except HouseNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="House id is invalid")
        return 204

    @route.post("/{house_id}/sale", url_name="saveSalePrice", response={204: None})
    def save_sale_price(self, house_id: str, sale_price: UpdateHouseSalePriceInSchema):
        """
        ## Params
            house_id(매물 id)\n

        ## Body
            sale_price(매물 매매가)\n
        """
        try:
            services.update_house_sale_price(house_id, **sale_price.__dict__)
        except HouseNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="House id is invalid")
        return 204

    @route.get(
        "/default-options",
        url_name="getAllOptions",
        response=ListHouseDefaultOptionsOutSchema,
    )
    def get_all_default_house_options(self):
        house_options = services.get_default_house_options_list()
        return house_options

    @route.post(
        "/{house_id}/selected-options",
        url_name="saveAllOptions",
        response={204: None},
    )
    def save_selected_house_options(
        self, house_id: str, selected_option: UpdateHouseSelectedOptionsInSchema
    ):
        """
        ## Params
            house_id(매물 id)\n

        ## Body
            type(주거형태 옵션)
            floor(층수 옵션)
            room(룸형태 옵션)
            restroom(화장실 옵션)
            duplex(복층 옵션)\n
        """
        try:
            services.update_house_options(house_id, **selected_option.__dict__)
        except HouseNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="House id is invalid")
        return 204

    @route.post("/{house_id}/image", url_name="saveImage")
    async def save_house_images(self, house_id: str, files: List[UploadedFile] = File(...)):
        return
