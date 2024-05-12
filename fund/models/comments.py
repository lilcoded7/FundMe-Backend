from setup.basemodel import TimeBaseModel
from fund.models.fundme import FundMe
from django.db import models

class CommentReaction(TimeBaseModel):
    profile = models.ImageField(null=True, blank=True)
    username = models.CharField(max_length=100)
    message = models.CharField(max_length=100, null=True, blank=True)
    emaji = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username