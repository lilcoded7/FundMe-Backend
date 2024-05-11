from setup.basemodel import TimeBaseModel
from django.db import models


class Event(TimeBaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.name