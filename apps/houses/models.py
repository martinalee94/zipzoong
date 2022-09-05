from django.db import models


class House(models.Model):
    type = models.CharField(verbose_name="주거 형태", max_length=4, null=True, db_index=True)
    contract_type = models.CharField(verbose_name="판매 유형", max_length=4, null=True, db_index=True)
    sell_price = models.IntegerField(verbose_name="매매가", null=True)
