from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Seller(models.Model):
    id = models.CharField(max_length=128, primary_key=True, verbose_name="server-key")
    nickname = models.CharField(max_length=20, unique=True, null=True)
    phone = models.CharField(max_length=11, null=True)
    client_secret = models.CharField(max_length=12, unique=True, verbose_name="client-key")
    created_dt = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_dt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid4())
        return super().save(*args, **kwargs)

    @classmethod
    def client_secret_get_or_none(cls, client_secret):
        try:
            seller = cls.objects.get(client_secret=client_secret)
        except ObjectDoesNotExist:
            return None
        return seller

    class Meta:
        db_table = "zipzoong_seller"


class Notice(models.Model):
    priority = models.IntegerField(null=True)
    title = models.CharField(max_length=500)
    contents = models.TextField()
    type = models.IntegerField()
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "zipzoong_notice"


class Qna(models.Model):
    priority = models.IntegerField(null=True)
    question = models.CharField(max_length=500)
    answer = models.TextField()
    type = models.IntegerField()
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "zipzoong_qna"
