from setup.basemodel import TimeBaseModel
from django.db import models

class Volunteer(TimeBaseModel):
    STATUS = [
        ('Voluntesr', 'Volunteer'),
        ('Donner', 'Donner')
    ]
    image = models.ImageField(null=True, blank=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.name
    
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 