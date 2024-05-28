from setup.basemodel import TimeBaseModel
from django.db import models


class Company(TimeBaseModel):
    name = models.CharField(max_length=100)
    logo = models.ImageField()
    wallet = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    











    