from django.db import models

from apps.commons.models import TimeStampModel
from apps.users.models import Seller


class House(TimeStampModel, models.Model):
    id = models.CharField(verbose_name="집 일련번호", primary_key=True, max_length=32)
    type = models.CharField(verbose_name="주거 형태", max_length=4, db_index=True)
    contract_type = models.CharField(verbose_name="판매 유형", max_length=4, db_index=True)
    sell_price = models.CharField(verbose_name="매매가", max_length=256, null=True)
    charter_rent_price = models.CharField(verbose_name="전세가", max_length=256, null=True)
    monthly_rent_price = models.IntegerField(verbose_name="월세가", null=True)
    deposit_rent_price = models.IntegerField(verbose_name="보증금", null=True)
    sido_addr = models.CharField(verbose_name="시도", max_length=32)
    gungu_addr = models.CharField(verbose_name="군구", max_length=32)
    street_addr = models.CharField(verbose_name="도로명", max_length=128)
    detail_addr = models.CharField(verbose_name="상세주소", max_length=256)
    postal_code = models.CharField(verbose_name="우편번호", max_length=6)
    seller = models.ForeignKey(Seller, related_name="seller", db_index=True)


class HouseOption(TimeStampModel, models.Model):
    id = models.CharField(verbose_name="집 일련번호", primary_key=True, max_length=32)
    # TODO: 옵션 종류 협의 필요


class HouseImage(TimeStampModel, models.Model):
    house = models.ForeignKey(House, related_name="")
    path = models.CharField(verbose_name="사진 경로", max_length=256)
    name = models.CharField(verbose_name="사진명", max_length=256)
    extension = models.CharField(verbose_name="사진 확장자", max_length=256)
    size = models.IntegerField(verbose_name="사진 사이즈")
    width = models.IntegerField(verbose_name="사진 가로 길이")
    height = models.IntegerField(verbose_name="사진 세로 길이")
    wh_type = models.SmallIntegerField(verbose_name="사진 크기 타입")
