from django.urls import path
from fund.views import * 


urlpatterns = [
    path('', home, name='home')
]

