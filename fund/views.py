from django.shortcuts import render, get_object_or_404
from fund.models.fundme import FundMe
from fund.serializers import * 
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from fund.models.fundimages import Fundimage
from fund.models.comments import CommentReaction
from fund.models.sponsorships import Sponsorship
from setup.permissions import IsApexAdmin
from fund.notifications import EmailSender
from accounts.models import Gender
from accounts.serializers import GenderSerializer
from fund.models.category import Category
from fund.models.organizations import OrganizationCategory
from pypaystack import Transaction
from pypaystack.errors import InvalidDataError
from fund.models.transactions import Transactions
from fund.models.organfunme import OrganFund
from fund.models.company import Company
from django.db.models import Sum 
import random

# Create your views here.


class ListRetrievefundMedoneAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = FundMe.objects.all()
    serializer_class = FundMeSerializer
    permission_classes = [AllowAny]

class ListOrganizationCategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category = OrganizationCategory.objects.all()
        serializer = OrganizationsCategorySerializer(category, many=True)
        return Response({'org_category':serializer.data}, 200)

class ListRetrieveGenderAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    permission_classes = [AllowAny]
    

class CreateFundMeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = FundMeSerializer
    permission_classes  = [IsAuthenticated]
    queryset = FundMe.objects.all()


class CreateSponsorshipViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SponsorshipSerializer
    permission_classes  = [IsAuthenticated]
    queryset = Sponsorship.objects.all()

    
class ListRetrieveSponsorshipAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer
    permission_classes = [AllowAny]

    
class ListRetrieveFundImagesAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Fundimage.objects.all()
    serializer_class = FundImagesSerializer
    permission_classes = [AllowAny]


class ListRegiriveCategoryApiView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.all()


class ListRegiriveCommentsApiView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = CommentsSerializer
    permission_classes = [AllowAny]
    queryset = CommentReaction.objects.all()



class ListOrRetreiveDonerDonationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = DonerDonationFundMe
    permission_classes  = [AllowAny]
    queryset = Donation.objects.all()


class CommentAPIView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_username(self, request):
        if request.user.is_authenticated:
            username = request.user.username
        else:
            username = 'Anonymous'
        return username

    def post(self, request, fundme_id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            fundme = get_object_or_404(FundMe, id=fundme_id)
            username = self.get_username(request)

            CommentReaction.objects.create(fundme=fundme, username=username, message=serializer.data['message'])
            return Response({'message': 'Commented'}, status=200)
        return Response({'message': 'Failed to comment', 'errors': serializer.errors}, status=400)


class DonationApiView(generics.GenericAPIView):
    serializer_class = DonationSerializer
    permission_classes = [AllowAny]

    def get_doner_name(self, request):
        if request.user.is_authenticated:
            user = request.user
            EmailSender.donation_sucess(user)
            doner_name = user.username

        else:
            doner_name = 'Anonymous'
        print('we are donation here')
        return doner_name

    def post(self, request, fundme_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            fundme = get_object_or_404(FundMe, id=fundme_id)
            
            doner_name = self.get_doner_name(request)

             
            Donation.objects.create(donor_fullname=doner_name, amount=serializer.validated_data['amount'], fundme=fundme)
            return Response({'message': 'Amount Donated Successfully'}, status=200)
        return Response({'message': serializer.errors}, status=400)
    



class OrganizationApiView(generics.GenericAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        organization = Organization.objects.filter(id=user.organization ,is_active=True)
        return Response({'organization':self.serializer_class(organization, many=True).data})
        

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            organization = serializer.save()
            user.organization=organization
            user.save()
            return Response({'message':'Your Request Has Been Received, We Are Currently viewing Your Request'}, 200)
        return Response({'messages':serializer.errors}, 400)
    

class ListUpdateDeleteOrganizationApiView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = Organization
    permission_classes  = [IsApexAdmin]
    queryset = Organization.objects.all()

from decimal import Decimal

class TransactionAPIView(generics.GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [AllowAny]

    def transaction_id(self):
        return random.randint(0, 99999999)  # Ensure the range is correct

    def process_transaction(self, data):
        try:
            amount = Decimal(data['amount'])  # Convert to Decimal
            transaction = Transaction(authorization_key='sk_live_d4039e928f5d4d81fe00acd97652fed8c60325b3')
            transaction.charge(
                email='lilcoded7@gmail.com',
                auth_code=str(self.transaction_id()),
                amount=int(amount * 100)
            )
            return transaction.verify(str(self.transaction_id()))
        except InvalidDataError as e:
            print(f"InvalidDataError: {e}")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            if not self.process_transaction(data):
                return Response({'message': 'Transaction Failed to process'}, status=400)
          
            return Response({'message': 'Amount Donated Successfully'}, status=200)
        return Response({'message': serializer.errors}, status=400)


class FundMeAnalyticsAPIView(APIView):
    def total_fundme(self):
        fundme = FundMe.objects.all()
        return fundme.count()

    def total_organization(self):
        organization = Organization.objects.all()
        return organization.count()
    
    def total_sponsorship(self):
        sponsorship = Sponsorship.objects.all()
        return sponsorship.count()
    
    def total_donations(self):
        return Donation.objects.aggregate(total=Sum('amount'))['total']

    def all_time_profit(self):
        return Company.objects.aggregate(total=Sum('wallet'))['total']
    
    def get_total_individual_organization(self):
        return Organization.objects.filter(category_name='Individual').count()
    
    def get_total_charity_organization(self):
        return Organization.objects.filter(category_name='Charity').count()
    

    def get(self, request):
        
        request_body = {
            'total_fundme':self.total_fundme(),
            'total_organization':self.total_organization(),
            'total_sponsorship':self.total_sponsorship(),
            'total_transaction':self.total_transaction(),
            'get_total_individual_organization':self.get_total_individual_organization(),
            'get_total_charity_organization':self.get_total_charity_organization(),
            'all_time_profit':self.all_time_profit()
        }
        return Response({'analysis':request_body})



class ListDonationfundMedoneAPIView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]



class OrganizationFundMeAnalysisApiView(APIView):
    permission_classes = [IsAuthenticated]

    def total_donations_for_organization(self, organization_id):
            
        fundme_ids = OrganFund.objects.filter(organization_id=organization_id).values_list('fundme_id', flat=True)
        
        total_donations = Donation.objects.filter(fundme_id__in=fundme_ids).aggregate(total_amount=Sum('amount'))
        
        return total_donations['total_amount'] if total_donations['total_amount'] is not None else 0.00


    def get_organization(self, organization):
        return get_object_or_404(Organization, id=organization.id)

    def get_all_organ_fundme(self, org_fundme):

        return [
            {
                'organ_fundme':FundMeSerializer(FundMe.objects.filter(id=fund.id), many=True).data
            }
            for fund in org_fundme
        ]
  
    def get(self, request):
        user = request.user 

        organization = OrganFund.objects.filter(organization=user.organization.id)

        return Response([
            {
                'total_org_fundme':organization.count(),
                'organ_fundme':self.get_all_organ_fundme(organization),
                'organization':OrganizationSerializer(self.get_organization(user.organization)).data,
                'total_amount_raised':self.total_donations_for_organization(user.organization.id)
            }
        ])

