from setup.basemodel import TimeBaseModel
from django.db import models
from fund.models.images_category import ImageCategory


class Fundimage(TimeBaseModel):
    image = models.ImageField()
    sub_description = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(ImageCategory, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return str(self.id)