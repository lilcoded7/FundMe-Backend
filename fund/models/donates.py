from setup.basemodel import TimeBaseModel
from fund.models.fundme import FundMe
from django.db import models

class Donation(TimeBaseModel):
    donor_fullname = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fundme = models.ForeignKey(FundMe, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.donor