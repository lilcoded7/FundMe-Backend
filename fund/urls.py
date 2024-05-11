from django.urls import path, include
from fund.views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Admin routes
router.register("", FundMeViewSet, basename='fundme')

urlpatterns = []


urlpatterns = [
    path("fundme/", include(router.urls)),
]

