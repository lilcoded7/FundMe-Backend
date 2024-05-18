from django.contrib import admin
from accounts.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Gender)


admin.site.site_header = 'Fund Me'
admin.site.site_title = 'Fund Me'

# Customize the site index text (optional)
admin.site.index_title = 'Welcome to Fund Me Admin'



admin.site.register(LoggedInUserDevices)
admin.site.register(UserVerificationCode)