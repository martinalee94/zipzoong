from django.db import models

from apps.commons.models import TimeStampModel
from apps.users.models import Agent, Seller


class House(TimeStampModel, models.Model):
    # id = models.CharField(verbose_name="집 일련번호", primary_key=True, max_length=32)
    type = models.CharField(verbose_name="주거 형태", max_length=4, null=True, db_index=True)
    contract_type = models.CharField(verbose_name="판매 유형", max_length=4, null=True, db_index=True)  # TODO: null값 허용?
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
        Seller,
        related_name="house",
        on_delete=models.SET_DEFAULT,
        db_index=True,
        default="deleted",
    )

    class Meta:
        db_table = "house"


class HouseOption(TimeStampModel, models.Model):
    house = models.OneToOneField(
        House,
        related_name="options",
        on_delete=models.CASCADE,
    )
    # TODO: 옵션 종류 협의 필요
    aircon = models.SmallIntegerField(verbose_name="냉장고")

    class Meta:
        db_table = "house_option"


class HouseImage(TimeStampModel, models.Model):
    house = models.OneToOneField(House, related_name="images", on_delete=models.CASCADE)
    path = models.CharField(verbose_name="사진 경로", max_length=256)
    name = models.CharField(verbose_name="사진명", max_length=256)
    type = models.CharField(verbose_name="사진 확장자", max_length=256)
    size = models.IntegerField(verbose_name="사진 사이즈")
    width = models.IntegerField(verbose_name="사진 가로 길이")
    height = models.IntegerField(verbose_name="사진 세로 길이")
    wh_type = models.SmallIntegerField(verbose_name="사진 크기 타입")

    class Meta:
        db_table = "house_image"


class HouseBidInfo(TimeStampModel, models.Model):
    yes_no = [("Y", "Yes"), ("N", "No")]
    house = models.ForeignKey(House, related_name="bid_info", on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, related_name="bid_info", on_delete=models.CASCADE)
    bid_price = models.IntegerField(verbose_name="중개 수수료 입찰가")
    contact_req = models.CharField(
        verbose_name="연락요청 여부",
        max_length=2,
        choices=yes_no,
        default="N",
    )
    success_bid = models.CharField(
        verbose_name="낙찰 성공 여부",
        max_length=2,
        choices=yes_no,
        default="N",
    )
    kind_rating = models.SmallIntegerField(verbose_name="친절도")
    speed_rating = models.SmallIntegerField(verbose_name="빠른 처리")
    cost_rating = models.SmallIntegerField(verbose_name="가격 경쟁력")
    time_rating = models.SmallIntegerField(verbose_name="시간 준수")
    quality_rating = models.SmallIntegerField(verbose_name="매물 퀄리티")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["house", "agent"], name="unique_bid"),
        ]
