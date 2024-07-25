from setup.basemodel import TimeBaseModel
from django.db import models

class Category(TimeBaseModel):
    CATE_STATUS = [
        ('Government', 'Government'),
        ('Private', 'Private'),
        ('None-Profit', 'None-Profit'),
        ('Personal', 'Personal'),
        ('Emergency', 'Emergency'),
        ('National Funding', 'National Funding')
    ]
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=CATE_STATUS, null=True, blank=True)

    def __str__(self):
        return self.name
    

    