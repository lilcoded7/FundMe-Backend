from setup.basemodel import TimeBaseModel
from django.db import models

class ImageCategory(TimeBaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

    