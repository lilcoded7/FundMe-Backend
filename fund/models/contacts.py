from django.db import models
from setup.basemodel import TimeBaseModel
from fund.models.organizations import Organization

class Contact(TimeBaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    organizer = models.ForeignKey(Organization, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return self.name 