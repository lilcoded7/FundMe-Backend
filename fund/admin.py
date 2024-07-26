from django.contrib import admin
from fund.models.category import Category
from fund.models.organizations import Organization, OrganizationCategory, BankAccount
from fund.models.fundme import FundMe
from fund.models.sponsorships import Sponsorship
from fund.models.fundimages import Fundimage
from fund.models.images_category import ImageCategory
from fund.models.events import Event
from fund.models.donates import Donation
from fund.models.comments import CommentReaction
from fund.models.transactions import Transactions
from fund.models.organfunme import OrganFund
from fund.models.contacts import Contact
from fund.models.sliders import Slider
from fund.models.chat_bot import ChatBot
# Register your models here.



admin.site.register(Slider)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Organization)
admin.site.register(FundMe)
admin.site.register(Sponsorship)
admin.site.register(Fundimage)
admin.site.register(ImageCategory)
admin.site.register(Donation)
admin.site.register(OrganizationCategory)
admin.site.register(Event)
admin.site.register(CommentReaction)
admin.site.register(Transactions)
admin.site.register(OrganFund)
admin.site.register(BankAccount)
admin.site.register(ChatBot)