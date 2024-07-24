from setup.basemodel import TimeBaseModel
from fund.models.organizations import Organization
from django.db import models


class Transactions(TimeBaseModel):
    TYPE = [
        ('withdraw', 'withdraw')
    ]

    status = models.CharField(max_length=60, choices=TYPE, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    trans_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name



