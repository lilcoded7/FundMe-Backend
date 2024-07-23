from setup.basemodel import TimeBaseModel
from django.conf import settings
from django.db import models



class OrganizationCategory(TimeBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Organization(TimeBaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
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


class BankAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=500)
    branch_code = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.bank_name