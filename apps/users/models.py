import uuid

from django.db import models

from apps.commons.models import TimeStampModel


class Seller(TimeStampModel, models.Model):
    def create_uuid():
        try:
            while True:
                uniq_uuid = uuid.uuid4()
                Seller.objects.get(uniq_num=uniq_uuid)
        except Exception:
            return uniq_uuid

    id = models.CharField(verbose_name="판매자 일련번호", primary_key=True, max_length=32, db_index=True)
    uniq_num = models.CharField(verbose_name="판매자 고유넘버", max_length=36, unique=True, db_index=True, default=create_uuid)
    nickname = models.CharField(verbose_name="판매자 닉네임", max_length=20, null=True)
    phone = models.CharField(verbose_name="판매자 전화번호", max_length=11, null=True)

    class Meta:
        db_table = "seller"


class Agent(TimeStampModel, models.Model):
    id = models.CharField(verbose_name="중계사 일련번호", primary_key=True, max_length=32)

    class Meta:
        db_table = "agent"
