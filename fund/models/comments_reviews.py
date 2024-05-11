from setup.basemodel import TimeBaseModel
from fund.models.fundme import FundMe
from django.db import models

class CommentReaction(TimeBaseModel):
    donor = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    react = models.ImageField()

    def __str__(self):
        return self.donor