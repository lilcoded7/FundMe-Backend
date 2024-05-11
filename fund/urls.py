from django.urls import path, include
from fund.views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Admin routes
router.register("", FundMeViewSet, basename='fundme')
router.register("create", CreateFundMeViewSet, basename='createfundme')
router.register("images/coded", FundImagesViewSet, basename='fundimages')

urlpatterns = []


urlpatterns = [
    path("fundme/", include(router.urls)),
]

