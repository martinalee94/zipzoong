from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.commons.models import TimeStampModel
from apps.users.models import Agent, Seller
from apps.users.utils import get_seller_from_header


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


class HouseOption(TimeStampModel, models.Model):
    house = models.OneToOneField(House, related_name="options", on_delete=models.CASCADE)
    # TODO: 옵션 종류 협의 필요
    aircon = models.SmallIntegerField(verbose_name="에어컨", null=True)
    bath = models.SmallIntegerField(verbose_name="화장실", null=True)

    class Meta:
        db_table = "house_option"


@receiver(post_save, sender=House)
def create_house(sender, instance, created, **kwargs):
    if created:
        HouseOption.objects.create(house=instance)


class HouseImage(TimeStampModel, models.Model):
    def get_upload_path(instance, filename):
        filetype = filename.split(".")[-1]
        device = instance.house.seller.device
        house_id = instance.house.id
        idx = HouseImage.objects.filter(house__id=house_id).count() + 1
        return f"house/{device}/{house_id}/{idx}.{filetype}"

    house = models.ForeignKey(House, related_name="images", unique=False, on_delete=models.CASCADE)
    path = models.ImageField(
        verbose_name="사진경로",
        blank=True,
        upload_to=get_upload_path,
        width_field="width",
        height_field="height",
    )
    # name = models.CharField(verbose_name="사진명", max_length=256, editable=False)
    type = models.CharField(verbose_name="사진 확장자", max_length=256, editable=False, default="png")
    size = models.IntegerField(verbose_name="사진 사이즈", editable=False)
    width = models.IntegerField(verbose_name="사진 가로 길이", editable=False)
    height = models.IntegerField(verbose_name="사진 세로 길이", editable=False)
    wh_type = models.SmallIntegerField(verbose_name="사진 크기 타입", editable=False, default=0)

    class Meta:
        db_table = "house_image"
