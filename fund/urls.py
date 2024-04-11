from django.urls import path
from fund.views import * 


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('causes/<str:causes_id>', causes, name='causes'),
    path('causes/details/<str:causes_id>', causes_details, name='causes_details')
]

