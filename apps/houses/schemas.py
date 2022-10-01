from ninja_schema import ModelSchema, Schema


class DefaultOutSchema(Schema):
    respCode: int


class CreateHouseAddressInSchema(Schema):
    seller_id: str
    sido_addr: str
    gungu_addr: str
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
    contract_type: list = None
    house_type: list = None
    floor: list = None
    room: list = None
    restroom: list = None
    duplex: list = None


class UpdateHouseSelectedOptionsInSchema(Schema):
    type: str = None
    floor: str = None
    room: str = None
    restroom: str = None
    duplex: str = None
