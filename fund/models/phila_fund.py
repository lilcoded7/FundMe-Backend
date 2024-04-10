from setup.basemodel import TimeBaseModel
from fund.models.category import Category
from django.db import models 


class PhilaFund(TimeBaseModel):
    image = models.ImageField()
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    raised = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    earned = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return self.title
    

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 

    