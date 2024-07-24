from setup.basemodel import TimeBaseModel
from django.db import models


class Slider(TimeBaseModel):
    image = models.ImageField()
    name_or_time = models.CharField(max_length=100, null=True, blank=True)
    sub_name = models.CharField(max_length=100, null=True, blank=True)
    slogan = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        
        return self.name_or_time
