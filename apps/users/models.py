from django.db import models

from apps.commons.models import TimeStampModel


class Seller(TimeStampModel, models.Model):
    id = models.CharField(
        verbose_name="판매자 일련번호", primary_key=True, max_length=32, db_index=True
    )
    uniq_num = models.CharField(verbose_name="판매자 고유넘버", max_length=16, db_index=True)
    nickname = models.CharField(verbose_name="판매자 닉네임", max_length=20, null=True)
    phone = models.CharField(verbose_name="판매자 전화번호", max_length=11, null=True)


class Agent(TimeStampModel, models.Model):
    id = models.CharField(verbose_name="중계사 일련번호", primary_key=True, max_length=32)
