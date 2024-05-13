from setup.basemodel import TimeBaseModel
from django.db import models


class Sponsorship(TimeBaseModel):
    STATUS = [
        ('Philantropist', 'Philantropist'),
        ('Donner', 'Donner')
    ]
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.name
    
    