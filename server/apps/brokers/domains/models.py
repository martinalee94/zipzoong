from django.db import models

from apps.commons.models import TimeStampModel


class Brokers(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    position = models.CharField(max_length=32, null=True)
    association = models.CharField(max_length=64, null=True)
    license_num = models.CharField(max_length=32, null=True)
    phone = models.CharField(max_length=20, null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        db_table = "broker"


class BrokerImages(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    broker = models.ForeignKey(Brokers, on_delete=models.CASCADE)
    path = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=256, null=True)
    type = models.CharField(max_length=32, null=True)
    size = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        db_table = "broker_image"
