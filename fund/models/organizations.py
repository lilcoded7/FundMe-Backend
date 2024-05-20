from setup.basemodel import TimeBaseModel
from fund.models.fundme import FundMe
from fund.models.category import Category
from django.db import models


class OrganizationCategory(TimeBaseModel):
    name = models.CharField(max_length=100)


class Organization(TimeBaseModel):
    fundme = models.ForeignKey(FundMe, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(OrganizationCategory, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    location = models.CharField(max_length=100)
    no_of_staff = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    cert = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'Organization: {self.name} Location: {self.location}'








