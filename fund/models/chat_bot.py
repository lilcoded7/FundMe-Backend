from django.db import models
from setup.basemodel import TimeBaseModel


class ChatBot(TimeBaseModel):
    organization_name = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    web_site = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.organization_name