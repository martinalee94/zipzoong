from django.db import models

from apps.commons.models import TimeStampModel


class Seller(TimeStampModel, models.Model):
    device = models.CharField(
        verbose_name="판매자 핸드폰 고유 넘버", max_length=36, unique=True, db_index=True, blank=False
    )
    nickname = models.CharField(verbose_name="판매자 닉네임", max_length=20, null=True)
    phone = models.CharField(verbose_name="판매자 전화번호", max_length=11, null=True)

    REQUIRED_FIELDS = ["device"]

    class Meta:
        db_table = "seller"


class Agent(TimeStampModel, models.Model):
    class Meta:
        db_table = "agent"
