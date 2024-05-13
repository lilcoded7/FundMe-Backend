from django.urls import path, include
from fund.views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Admin routes
router.register("", FundMeViewSet, basename='fundme')
router.register("create", CreateFundMeViewSet, basename='createfundme')
router.register("images/coded", FundImagesViewSet, basename='fundimages')
router.register("comment", CommentViewSet, basename='comment')
router.register("doner/donation/fundme", ListOrRetreiveDonerDonationViewSet, basename='doner_donation_fundme')
router.register('organization', ListUpdateDeleteOrganizationViewSet, basename='origanization')

urlpatterns = []


urlpatterns = [
    path("fundme/", include(router.urls)),
    path('donation/', DonationApiView.as_view(), name='donation'),
    path('organizations/', OrganizationApiView.as_view(), name='organizations')
]

