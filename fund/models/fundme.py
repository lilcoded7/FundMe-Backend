from setup.basemodel import TimeBaseModel
from fund.models.category import Category
from django.conf import Settings
from django.db import models 


class FundMe(TimeBaseModel):
    image = models.ImageField()
    title = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=100, null=True, blank=True)
    target = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    raised = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True)

    def __str__(self) -> str:
        return self.title
    
