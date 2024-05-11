from django.contrib import admin
from fund.models.category import Category
from fund.models.organizations import PartnerShip
from fund.models.fundme import FundMe
from fund.models.volunteers import Volunteer
# Register your models here.



admin.site.register(Category)
admin.site.register(PartnerShip)
admin.site.register(FundMe)
admin.site.register(Volunteer)