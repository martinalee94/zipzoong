from apps.users.models import Seller
from django.test import Client, TestCase


def test_save_client_id():
    Seller()
