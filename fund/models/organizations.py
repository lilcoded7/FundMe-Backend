from setup.basemodel import TimeBaseModel
from django.db import models


class PartnerShip(TimeBaseModel):
    PARTNER_STATUS = [
        ('Charity Organization', 'Charity Organization'), 
        ('Individual', 'Individual')
    ]

    image = models.ImageField()
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=PARTNER_STATUS)
    cert = models.FileField(null=True, blank=True)
