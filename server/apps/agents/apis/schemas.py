from apps.houses.apis.schemas import ListHouseInfoListOutSchema
from ninja import Field
from ninja_schema import Schema


class AgentSignUpSchema(Schema):
    email: str
    password: str
    confirmed_password: str
    name: str


class AgentSignUpOutSchema(Schema):
    email: str
    access_token: str

    # email: constr(regex=r"^[\w\.-]+@([\w]+\.-)+[\w]-{2,4}$")
    # @validator("confirmed_password", allow_reuse=True)
    # def password_match(cls, confirmed_password, values, **kwargs):
    #     if confirmed_password != values["password"]:
    #         raise ValidationError("Password and confirmed password are not matched.")
    #     return confirmed_password
    # class Config:
    #     arbitrary_types_allowed = True


class AgentDetailInSchema(Schema):
    position: str
    association: str
    agent_license_num: str


class AgentHouseList(Schema):
    page_num: int = Field(..., description="시작페이지넘버")
    num: int = Field(..., description="순서")
    house_info: dict = Field(None, description="순서")
