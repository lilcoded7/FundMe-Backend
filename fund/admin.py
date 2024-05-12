from django.contrib import admin
from fund.models.category import Category
from fund.models.organizations import PartnerShip
from fund.models.fundme import FundMe
from fund.models.volunteers import Volunteer
from fund.models.fundimages import Fundimage
from fund.models.images_category import ImageCategory
from fund.models.events import Event
from fund.models.donates import Donation
from fund.models.comments import CommentReaction

# Register your models here.



admin.site.register(Category)
admin.site.register(PartnerShip)
admin.site.register(FundMe)
admin.site.register(Volunteer)
admin.site.register(Fundimage)
admin.site.register(ImageCategory)