from django.db import models
from django.contrib.auth import get_user_model

from account.enums import ExchangeEnum
# Create your models here.

User = get_user_model()


class Info(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Coinex
    coinex_access_id = models.CharField(max_length=128, null=True, blank=True)
    coinex_secret_key = models.CharField(max_length=128, null=True, blank=True)

    # Kucoin
    kucoin_key = models.CharField(max_length=128, null=True, blank=True)
    kucoin_secret = models.CharField(max_length=128, null=True, blank=True)
    kucoin_passphrase = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'info'

    def __str__(self) -> str:
        return f"{self.user}"
