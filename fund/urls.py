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
router.register('sponsorship', ListRetrieveSponsorshipViewSet, basename='sponsorship')
router.register('list/donation', ListDonationfundMedoneAPIView, basename='listdonation')
router.register('list/commets', ListRegiriveCommentsApiView, basename='list_comments')
router.register('create/sponsorship', CreateSponsorshipViewSet, basename='create_sponshorship')
router.register('create/bank/account', CreateBankAccountViewSet, basename='bankaccount')
router.register('bank/retrieve/account', ListRetrieveBankAccountViewSet, basename='listbankaccount')
router.register('sliders/', SliderViewSet, basename='slider')


urlpatterns = [
    path("fundme/", include(router.urls)),
    path('donate/<int:fundme_id>/', DonationApiView.as_view(), name='donate'),
    path('organizations/', OrganizationApiView.as_view(), name='organizations'),
    path('organization/categorys', ListOrganizationCategoryAPIView.as_view(), name='organizationcategory'),
    path('analysis/', FundMeAnalyticsAPIView.as_view(), name='analysis'),
    path('list/organization/fundme/analysis/', OrganizationFundMeAnalysisApiView.as_view(), name='org_analysis'),
    path('comment/<int:fundme_id>/', CommentAPIView.as_view(), name='comment'),
    path('organization/create/fundme/', CreateOrganizationFundMe.as_view(), name='create_organization_fundme'),
    path('List/organizations/by/category<str:fund_category_id>/', ListOrganizationsByCategory.as_view(), name='categor_org_fundme'),
    path('list/emergency/funds/', ListEmergencyFund.as_view(), name='list_emergency_fund'),
    path('list/all/fund/me/', ListActiveFundMeAPIView.as_view(), name='list_all_fund_me'),
    path('withdraw/organization/fundme/<str:organization_id>/', WithdrawFundAPIView.as_view(), name='withdraw_organ_amount'),
    path('transactions/<str:organization_id>/', TransactionsAPIView.as_view(), name='transactions'),
    path('organization_graph/<str:organization_id>/', organizationGraph.as_view(), name='organization_graph')
    
    
]

