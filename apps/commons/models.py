from django.db import models
from django.utils import timezone


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="생성 날짜", db_index=True, default=timezone.now
    )
    modified_at = models.DateTimeField(verbose_name="수정 날짜", auto_now=True)

    class Meta:
        abstract = True
