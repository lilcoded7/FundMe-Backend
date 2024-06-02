from django.urls import path, include
from fund.views import * 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

# Admin routes
router.register("create", CreateFundMeViewSet, basename='createfundme')
router.register("images/coded", ListRetrieveFundImagesAPIView, basename='fundimages')
router.register("doner/donation/fundme", ListOrRetreiveDonerDonationViewSet, basename='doner_donation_fundme')
router.register('organization', ListUpdateDeleteOrganizationApiView, basename='origanization')
router.register('gender', ListRetrieveGenderAPIView, basename='gender')
router.register('categories', ListRegiriveCategoryApiView, basename='category')
router.register('get/fundme', ListRetrievefundMedoneAPIView, basename='don')
router.register('sponsorship', ListRetrieveSponsorshipAPIView, basename='sponsorship')
router.register('list/donation', ListDonationfundMedoneAPIView, basename='listdonation')
router.register('list/commets', ListRegiriveCommentsApiView, basename='list_comments')
router.register('create/sponsorship', CreateSponsorshipViewSet, basename='create_sponshorship')


urlpatterns = [
    path("fundme/", include(router.urls)),
    path('donate/<int:fundme_id>/', DonationApiView.as_view(), name='donate'),
    path('organizations/', OrganizationApiView.as_view(), name='organizations'),
    path('transaction/', TransactionAPIView.as_view(), name='transaction'),
    path('organization/categorys', ListOrganizationCategoryAPIView.as_view(), name='organizationcategory'),
    path('analysis/', FundMeAnalyticsAPIView.as_view(), name='analysis'),
    path('list/organization/fundme/analysis/', OrganizationFundMeAnalysisApiView.as_view(), name='org_analysis'),
    path('comment/<int:fundme_id>/', CommentAPIView.as_view(), name='comment'),
    
]

