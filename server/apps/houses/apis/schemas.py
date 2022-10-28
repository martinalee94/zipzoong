from ninja import Field, Query
from ninja_schema import ModelSchema, Schema

from ..domains.models import HouseDetail, HouseImage, HouseOptionCode


class DefaultOutSchema(Schema):
    respCode: int


class CreateHouseAddressInSchema(Schema):
    full_jibun_addr: str = Field(..., description="서울 관악구 봉천동 896-28")
    full_street_addr: str = Field(..., description="서울 관악구 남부순환로214길 40")
    sido_addr: str = Field(..., description="서울")
    sigungu_addr: str = Field(..., description="서울 관악구")
    dong_addr: str = Field(..., description="서울 관악구 봉천동")
    street_addr: str = Field(..., description="남부순환로214길")
    detail_addr: str = Field(None, description="상세주소")
    postal_code: str = Field(None, description="우편번호")


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


class PaginationListSchema(Schema):
    page_num: int = Field(1, description="시작 페이지")
    info_num: int = Field(10, description="가져올 집 정보 개수")


class ListHouseInfoListOutSchema(Schema):
    address: str = Field(..., description="집주소")
    contract_type: str = Field(None, description="계약 형태")
    contract_detail: dict = Field(None, description="상세 계약 조건")
    options: ListHouseDefaultOptionsOutSchema = None
    images: ListHouseImagesOutSchema = None
