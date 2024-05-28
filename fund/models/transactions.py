from setup.basemodel import TimeBaseModel
from django.db import models


class Transactions(TimeBaseModel):
    name = models.CharField(max_length=100)
    trans_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.name
