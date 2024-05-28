from setup.basemodel import TimeBaseModel
from fund.models.organizations import Organization
from fund.models.fundme import FundMe
from django.db import models


class OrganFund(TimeBaseModel):
    fundme = models.ForeignKey(FundMe, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)