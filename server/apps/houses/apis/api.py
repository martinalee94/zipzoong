import asyncio
from datetime import datetime
from typing import List

from apps.commons.core import AuthBearer
from apps.commons.exceptions import APIException, APIExceptionErrorCodes
from ninja import Body, File, Query
from ninja.files import UploadedFile
from ninja_extra import api_controller, route

from ..exceptions import HouseNotFound, ImageSizeIsExceeded, ImageTypeIsNotAllowed, SellerNotFound
from ..services import services
from .schemas import (
    CreateHouseAddressInSchema,
    CreateHouseAddressOutSchema,
    PaginationListSchema,
    SellerHouseListOut,
    UpdateHouseCharterPriceInSchema,
    UpdateHouseMonthlyPriceInSchema,
    UpdateHouseSalePriceInSchema,
    UpdateHouseSelectedOptionsInSchema,
)


@api_controller("/houses", tags=["Houses"], auth=AuthBearer())
class HouseAPIController:
    @route.post("/address", url_name="saveAddress", response={200: CreateHouseAddressOutSchema})
    def save_address(
        self,
        addr_info: CreateHouseAddressInSchema,
        house_id: str = Query(None, description="매물 id"),
        seller_id: str = Body(..., description="의뢰인 서버쪽 id"),
    ):
        """
        ## Parms
            house_id ("매물 id") - Optional

        ## Body
            seller_id(의뢰인 서버쪽 id)
            full_jibun_addr : "서울 관악구 봉천동 896-28"
            full_street_addr: "서울 관악구 남부순환로214길 40"
            sido_addr: "서울"
            sigungu_addr:"서울 관악구"
            dong_addr: "서울 관악구 봉천동"
            street_addr : "남부순환로214길"
            detail_addr: 상세주소
            postal_code: 우편번호
        """
        try:
            house = services.add_house(
                house_id=house_id,
                seller_id=seller_id,
                addr_info=addr_info,
            )
        except SellerNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="Seller id is invalid")
        return CreateHouseAddressOutSchema.from_orm(house)

    @route.get(
        "/default-contract-type",
        url_name="getContractType",
    )
    def get_contract_type(self):
        contract_types = services.get_default_house_contract_type_list()
        return contract_types

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
        return

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
        return

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
        return

    @route.get(
        "/default-options",
        url_name="getAllOptions",
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
        return

    @route.post(
        "/media/{house_id}/image",
        url_name="saveImage",
        response={204: None},
    )
    async def save_house_images(self, house_id: str, images: List[UploadedFile] = File(...)):
        try:
            event_loop = []
            # for n, image in enumerate(images):
            #     event_loop.append(
            #         services.add_house_images(
            #             n=n, house_id=house_id, image=image, file_date_key=file_date_key
            #         )
            #     )
            # print(*event_loop)
            # await asyncio.gather(*event_loop)
            # for image in images:
            #     asyncio.create_task(
            #         services.add_house_images(
            #             house_id=house_id, image=image, file_date_key=file_date_key
            #         )
            #     )

            for num, image in enumerate(images):
                await services.add_house_images(house_id=house_id, image=image, num=num)
        except HouseNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="House id is invalid")
        except ImageSizeIsExceeded:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="Image is too big")
        except ImageTypeIsNotAllowed:
            raise APIException(
                APIExceptionErrorCodes.BAD_REQUEST,
                message="File type is not allowed - (jpg, jpeg, png)",
            )
        return

    @route.post("/list", url_name="getHouseInfo", response=List[SellerHouseListOut])
    def get_house_list(self, request, pagination: PaginationListSchema = Query(...)):
        try:
            result = services.get_house_info_list(request.auth, pagination=pagination)
        except HouseNotFound:
            raise APIException(APIExceptionErrorCodes.BAD_REQUEST, message="House id is invalid")
        return [
            SellerHouseListOut(page_num=pagination.page_num, num=i, house_info=result[i])
            for i in range(len(result))
        ]
