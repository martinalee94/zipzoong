from django.db import models

from apps.commons.models import TimeStampModel
from apps.users.models import Agent, Seller


class House(TimeStampModel, models.Model):
    type = models.CharField(verbose_name="주거 형태", max_length=4, null=True, db_index=True)
    contract_type = models.CharField(
        verbose_name="판매 유형", max_length=4, null=True, db_index=True
    )  # TODO: null값 허용?
    sell_price = models.IntegerField(verbose_name="매매가", null=True)
    charter_rent_price = models.IntegerField(verbose_name="전세가", null=True)
    monthly_rent_price = models.IntegerField(verbose_name="월세가", null=True)
    deposit_rent_price = models.IntegerField(verbose_name="보증금", null=True)
    full_addr = models.CharField(verbose_name="전체 주소", max_length=256)
    # TODO: 주소 어떻게 자를지 고민 필요함
    sido_addr = models.CharField(verbose_name="시도", max_length=32, null=True)
    gungu_addr = models.CharField(verbose_name="군구", max_length=32, null=True)
    street_addr = models.CharField(verbose_name="도로명", max_length=128, null=True)
    detail_addr = models.CharField(verbose_name="상세주소", max_length=256, null=True)
    postal_code = models.CharField(verbose_name="우편번호", max_length=6, null=True)
    seller = models.ForeignKey(
        Seller, related_name="house", on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        db_table = "house"
