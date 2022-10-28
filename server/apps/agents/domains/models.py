from apps.commons.models import TimeStampModel
from django.db import models


class Agent(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=12)
    password = models.CharField(max_length=64)

    position = models.CharField(max_length=32, null=True)
    association = models.CharField(max_length=64, null=True)
    license_num = models.CharField(max_length=32, null=True)
    phone = models.CharField(max_length=20, null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        db_table = "agent"


class AgentImage(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)
    path = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=256, null=True)
    type = models.CharField(max_length=32, null=True)
    size = models.IntegerField(null=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    created_dt = models.DateTimeField(verbose_name="생성 날짜", auto_now_add=True)
    modified_dt = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        db_table = "agent_image"
