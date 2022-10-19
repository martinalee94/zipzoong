from ninja_schema import ModelSchema, Schema

from ..domains.models import HouseDetail, HouseImage, HouseOptionCode


class DefaultOutSchema(Schema):
    respCode: int


class CreateHouseAddressInSchema(Schema):
    seller_id: str
    full_addr: str
    sido_addr: str
    sigungu_addr: str
    street_addr: str
    detail_addr: str = None
    postal_code: str = None


class CreateHouseAddressOutSchema(Schema):
    id: str


class UpdateHouseMonthlyPriceInSchema(Schema):
    deposit: int
    monthly_rent: int


class UpdateHouseCharterPriceInSchema(Schema):
    charter_rent: int


class UpdateHouseSalePriceInSchema(Schema):
    sale_price: int


class ListHouseDefaultOptionsOutSchema(ModelSchema):
    class Config:
        model = HouseDetail
        exclude = ["created_dt", "modified_dt"]


class ListHouseImagesOutSchema(ModelSchema):
    class Config:
        model = HouseImage
        include = ["path"]


class UpdateHouseSelectedOptionsInSchema(Schema):
    type: str = None
    floor: str = None
    room: str = None
    restroom: str = None
    duplex: str = None


class ListHouseInfoListInSchema(Schema):
    page_num: int
    info_num: int


class ListHouseInfoListOutSchema(Schema):
    address: str
    contract_type: str
    contract_detail: dict
    options: ListHouseDefaultOptionsOutSchema = None
    images: ListHouseImagesOutSchema = None
