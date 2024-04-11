from django.contrib import admin
from fund.models.category import Category
from fund.models.organizations import PartnerShip
from fund.models.phila_fund import PhilaFund
from fund.models.volunteers import Volunteer
# Register your models here.



admin.site.register(Category)
admin.site.register(PartnerShip)
admin.site.register(PhilaFund)
admin.site.register(Volunteer)