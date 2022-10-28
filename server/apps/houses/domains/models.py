from uuid import uuid4

from apps.users.domains.models import Seller
from django.db import models
from django.utils import timezone


class House(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    full_jibun_addr = models.CharField(max_length=128)
    full_street_addr = models.CharField(max_length=128)
    sido_addr = models.CharField(max_length=32)
    sigungu_addr = models.CharField(max_length=32)
    dong_addr = models.CharField(max_length=32)
    street_addr = models.CharField(max_length=128)
    detail_addr = models.CharField(max_length=256, null=True)
    postal_code = models.CharField(max_length=6, null=True)
    sale_price = models.PositiveIntegerField(null=True)
    contract_type = models.CharField(max_length=10, null=True)
    charter_rent = models.PositiveIntegerField(null=True)
    monthly_rent = models.PositiveIntegerField(null=True)
    monthly_deposit = models.PositiveIntegerField(null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", db_index=True, auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)
    seller = models.ForeignKey(
        Seller, to_field="id", on_delete=models.CASCADE, related_name="house"
    )

    @classmethod
    def create_house(cls, **kwargs):
        house = cls.objects.create(id=str(uuid4()), **kwargs)
        return house

    class Meta:
        db_table = "house"


class HouseOptionCode(models.Model):
    type = models.PositiveSmallIntegerField()
    key = models.PositiveIntegerField()
    value = models.CharField(max_length=50)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        db_table = "house_option_code"


class HouseDetail(models.Model):
    house = models.OneToOneField(
        House, to_field="id", on_delete=models.CASCADE, primary_key=True, related_name="detail"
    )
    type_option = models.CharField(max_length=20, null=True)
    floor_option = models.CharField(max_length=10, null=True)
    floor = models.SmallIntegerField(null=True)
    rooms_option = models.CharField(max_length=20, null=True)
    rooms = models.SmallIntegerField(null=True)
    restroom_option = models.CharField(max_length=10, null=True)
    rests = models.SmallIntegerField(null=True)
    duplex_option = models.CharField(max_length=10, null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        db_table = "house_detail"


class HouseImage(models.Model):
    house = models.ForeignKey(House, to_field="id", related_name="images", on_delete=models.CASCADE)
    path = models.CharField(verbose_name="사진 경로", max_length=256, null=True)
    name = models.CharField(verbose_name="사진명", max_length=256, null=True)
    type = models.CharField(verbose_name="사진 확장자", max_length=16, null=True)
    size = models.PositiveIntegerField(verbose_name="사진 사이즈", null=True)
    width = models.PositiveSmallIntegerField(verbose_name="사진 가로 길이", null=True)
    height = models.PositiveSmallIntegerField(verbose_name="사진 세로 길이", null=True)
    wh_type = models.SmallIntegerField(verbose_name="사진 크기 타입", null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)

    class Meta:
        db_table = "house_image"
