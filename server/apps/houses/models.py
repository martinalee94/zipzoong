from uuid import uuid4

from django.db import models


class House(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    sido_addr = models.CharField(max_length=32)
    gungu_addr = models.CharField(max_length=32)
    street_addr = models.CharField(max_length=128)
    detail_addr = models.CharField(max_length=256, null=True)
    postal_code = models.CharField(max_length=6, null=True)
    sale_price = models.PositiveIntegerField(null=True)
    charter_rent = models.PositiveIntegerField(null=True)
    monthly_rent = models.PositiveIntegerField(null=True)
    monthly_deposit = models.PositiveIntegerField(null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", db_index=True, auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    @classmethod
    def create_house(cls, **kwargs):
        house = cls.objects.create(id=str(uuid4()), **kwargs)
        return house

    class Meta:
        db_table = "house"


class HouseOptionCode(models.Model):
    type = models.PositiveSmallIntegerField()
    value = models.CharField(max_length=50, unique=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)

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
    pass
