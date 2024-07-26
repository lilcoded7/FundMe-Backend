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
from fund.models.transactions import Transactions
from fund.models.organfunme import OrganFund
from fund.models.company import Company
from django.db.models import Sum 
from decimal import Decimal
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncMonth
import random

# Create your views here.


class ListRetrievefundMedoneAPIView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = FundMe.objects.all()
    serializer_class = FundMeSerializer
    permission_classes = [AllowAny]


class SliderViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = FundMe.objects.all()
    serializer_class = SliderSerializer
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



class CreateBankAccountViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = BankAccountSerializer
    permission_classes  = [IsAuthenticated]
    queryset = BankAccount.objects.all()


class ListRetrieveBankAccountViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [AllowAny]

    
class ListRetrieveSponsorshipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
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

    def credit_organization_donation(self, fudnme, amount):

        organ_fundme = OrganFund.objects.get(fundme=fudnme)

        fund_amount = Decimal(amount)

        organ_fundme.organization.balance+=fund_amount
        
        organ_fundme.organization.save()

        return True


    def get_doner_name(self, request):
        if request.user.is_authenticated:
            user = request.user
            try:
                EmailSender.donation_sucess(user)
            except:
                pass
            doner_name = user.username

        else:
            doner_name = 'Anonymous'
    
        return doner_name

    def post(self, request, fundme_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            fundme = get_object_or_404(FundMe, id=fundme_id)

            amount=serializer.validated_data['amount']
            
            doner_name = self.get_doner_name(request)

            try:
                self.credit_organization_donation(fundme, amount)
            except:
                pass 
                
             
            Donation.objects.create(donor_fullname=doner_name, amount=amount, fundme=fundme)
            return Response({'message': 'Amount Funded Successfully'}, status=200)
        return Response({'message': serializer.errors}, status=400)
    



class OrganizationApiView(generics.GenericAPIView):
    serializer_class = CreateOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        organization = Organization.objects.filter(id=user.organization.id, is_active=True).first()

        if organization:
            serializer = OrganizationSerializer(organization, context={'request': request})
            return Response({'organization': serializer.data})
        else:
            return Response({'organization': None})

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
    serializer_class = OrganizationSerializer
    permission_classes  = [IsApexAdmin]
    queryset = Organization.objects.all()



class FundMeAnalyticsAPIView(APIView):
    def total_fundme(self):
        fundme = FundMe.objects.all()
        return fundme.count()

    def get_all_fundme(self):
        fundme = FundMe.objects.all()
        total_fundme = fundme.count()
        return  total_fundme
    
    def get_all_donation(self):
        donation = Donation.objects.all()
        total_donation_amount = donation.aggregate(total=Sum('amount'))['total']
        total_donation = donation.count()
        return total_donation if total_donation else 0, total_donation_amount if total_donation_amount else 0.00

    def total_sponsorship(self):
        sponsorship = Sponsorship.objects.all()
        total_sponsors = sponsorship.count()
        return total_sponsors if total_sponsors else 0
    
    def get_all_time_total_transactions_amount(self):

        total_pending_amount = Transactions.objects.filter(status='pending').aggregate(total=Sum('amount'))['total']
        total_credited_amount = Transactions.objects.filter(status='credited').aggregate(total=Sum('amount'))['total']

        return total_pending_amount if total_pending_amount else 0.00, total_credited_amount if total_credited_amount else 0.00

    def all_time_company_management(self):
        fundme_management = Company.objects.get(name='FundMe')
        return CompanySerializer(fundme_management).data
    

    def get(self, request):

        organization = Organization.objects.all()

        total_organization = organization.count()

        sponsorhips = Sponsorship.objects.all()
        total_sponsorhips = sponsorhips.count()

        all_fundme, total_fundme = self.get_all_fundme(request)

        total_donation_amount, total_donation  = self.get_all_donation()

        total_pending_amount, total_credited_amount = self.get_all_time_total_transactions_amount()
        
        request_body = {
            'total_organization':total_organization,
            'sponsorships':sponsorhips,
            'total_sponsorship':total_sponsorhips,
            'all_fundme':all_fundme,
            'total_fundme':total_fundme,
            'total_donation_amount':total_donation_amount,
            'total_donation':total_donation,
            'total_pending_amount':total_pending_amount,
            'total_credited_amount':total_credited_amount,
            'fundme_management':self.all_time_company_management(),

        }
        return Response({'analysis':request_body})
    

class ListOrganizationAdminAPIView(APIView):

    def status_type(self, request):
        status = request.query_params.get('status')
        start_date = None
        end_date = None
        organ_status = None

        if status == 'today':
            start_date = timezone.now().date()
            end_date = timezone.now().date()
        elif status == 'week':
            today = timezone.now().date()
            start_date = today - timezone.timedelta(days=today.weekday())
            end_date = start_date + timezone.timedelta(days=6)
        elif status == 'month':
            today = timezone.now().date()
            start_date = today.replace(day=1)
            end_date = today.replace(day=1) + timezone.timedelta(days=31)
            end_date = end_date.replace(day=1) - timezone.timedelta(days=1)
        elif status == 'active':
            organ_status = 'active'
        elif status == 'not active':
            organ_status = 'not active'
        else:
            return None, None, None  

        return start_date, end_date, organ_status
            

    def get(self, request):
        start_date, end_date, organ_status = self.status_type(request)

        if start_date and end_date:
            organ_filter = Organization.objects.filter(timestamp__date__range=[start_date, end_date])
        else:
            organ_filter = Organization.objects.all()

        if organ_status == 'active':
            organ_filter = organ_filter.filter(is_active=True)
        elif organ_status == 'not active':
            organ_filter = organ_filter.filter(is_active=False)

        organizations = OrganizationSerializer(organ_filter, many=True, context={'request': request})

        return Response({'organizations': organizations.data})

            

class ListTransactionsAdminAPIView(APIView):
    def status_type(self, request):
        status = request.query_params.get('status')
        start_date = None
        end_date = None
        trans_status = None

        if status == 'today':
            start_date = timezone.now().date()
            end_date = timezone.now().date()
        elif status == 'week':
            today = timezone.now().date()
            start_date = today - timezone.timedelta(days=today.weekday())
            end_date = start_date + timezone.timedelta(days=6)
        elif status == 'month':
            today = timezone.now().date()
            start_date = today.replace(day=1)
            end_date = (today.replace(day=1) + timezone.timedelta(days=31)).replace(day=1) - timezone.timedelta(days=1)
        elif status in ['Pending', 'Credited']:
            trans_status = status
        else:
            return None, None, None

        return start_date, end_date, trans_status

    def get(self, request):
        start_date, end_date, trans_status = self.status_type(request)

        if start_date and end_date:
            transactions = Transactions.objects.filter(timestamp__date__range=[start_date, end_date])
        else:
            transactions = Transactions.objects.all()

        if trans_status:
            transactions = transactions.filter(status=trans_status)

        serialized_transactions = TransactionsSerializer(transactions, many=True)
        
        return Response({'transactions': serialized_transactions.data})


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

    def get_all_organ_fundme(self, org_fundme, request):
        fundme= None
        total_org_fundme=None

        if org_fundme:
                
            
            fundme = FundMe.objects.filter(id=org_fundme.fundme.id)

            total_org_fundme = fundme.count()
        
        return FundMeSerializer(fundme, many=True, context={'request':request}).data, total_org_fundme
    
    def get_total_income(self, user):
        return Organization.objects.filter(id=user.organization.id).aggregate(total=Sum('balance'))['total']
    
    def get_organ_bank_account(self, user):
        bank_account = None
        try:
            bank_account = BankAccount.objects.get(user=user.id)
        except:
            pass 
        data = BankAccountSerializer(bank_account).data
        return data if data else 'Bank info Pending'
  
    def get(self, request):
        user = request.user 
        organization = OrganFund.objects.filter(organization=user.organization.id).first()

        serializer_context = {'request': request} 

        organ_fundme, total_organ_fundme = self.get_all_organ_fundme(organization, request)

        return Response([
            {
                'total_org_fundme': total_organ_fundme,
                'organ_fundme': organ_fundme,
                'organization': OrganizationSerializer(self.get_organization(user.organization), context=serializer_context).data,
                'total_amount_raised': self.total_donations_for_organization(user.organization.id),
                'all_time_amount_raised_wallet': self.get_total_income(user),
                'bank_account': self.get_organ_bank_account(user)
            }
        ])


class CreateOrganizationFundMe(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationCreateFundMeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = request.user

            if user.organization.is_active:
                fund_me = serializer.save()
                organ_funme = OrganFund.objects.create(
                    fundme=fund_me, organization=user.organization
                )
                if organ_funme:
                        
                    return Response({'message':'FundMe is currently under review, it will be live when approved'}, 200)
            return Response({'message':'Organization is not approved,  contact support info.fundmegh@gmail.com'}, 400)
        return Response({'message':serializer.errors}, 400)
    


class ListOrganizationsByCategory(APIView):
    def get(self, request, fund_category_id):  
        category = get_object_or_404(Category, id=fund_category_id)
        fundme = FundMe.objects.filter(category=category)
        serializer = FundMeSerializer(fundme, many=True, context={'request': request})
        return Response({'fundme': serializer.data}, 200)


class ListEmergencyFund(APIView):
    def get(self, request):
        fundme_queryset = FundMe.objects.filter(category__status='Emergency')

        serializer = FundMeSerializer(fundme_queryset, many=True, context={'request': request})
        data = serializer.data

        return Response({'data': data}, status=200)
    

class ListActiveFundMeAPIView(APIView):
    def get(self, request):

        fundme = FundMe.objects.filter(is_active=True)

        data = FundMeSerializer(fundme, many=True, context={'request': request}).data

        return Response({'fundme':data}, 200)




class WithdrawFundAPIView(APIView):
    serializer_class = WithdrawalSerializer

    def post(self, request, organization_id):
        print('request is passing ')
        try:
            organization = Organization.objects.get(id=organization_id)
           
        except Organization.DoesNotExist:
            return Response({'message': 'Organization not found'}, 400)

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data['amount']

            organ_balance = organization.balance

            if not organ_balance >= amount:
                return Response({'message': 'Insufficient balance'}, 400)
            
            num = random.randint(000000, 999999)

            organization.balance -= amount
            organization.save()

            transaction = Transactions.objects.create(
                status='Pending', organization=organization, trans_id=num, amount=amount
            )

            if transaction:
                return Response({'message': 'We are currently processing your withdrawal request'}, 200)

        return Response(serializer.errors, 400)    


class TransactionsAPIView(APIView):
    serializer_class = TransactionsSerializer

    def get(self, request, organization_id):
        filter_type = request.query_params.get('filter_type')

        if filter_type:
            if filter_type == 'today':
                start_date = timezone.now().date()
                end_date = timezone.now().date()
            elif filter_type == 'week':
                today = timezone.now().date()
                start_date = today - timezone.timedelta(days=today.weekday())
                end_date = start_date + timezone.timedelta(days=6)
            elif filter_type == 'month':
                start_date = timezone.now().replace(day=1).date()
                end_date = timezone.now().date()
            else:
                return Response({'message': 'Invalid filter_type'}, status=400)

            transactions = Transactions.objects.filter(
                organization_id=organization_id,
                timestamp__date__range=[start_date, end_date]
            )
        else:
            transactions = Transactions.objects.filter(organization_id=organization_id)

        serializer = self.serializer_class(transactions, many=True)
        return Response(serializer.data)


class organizationGraph(APIView):
    serializer_class = DonationSerializer

    def get(self, request, organization_id):
        try:
            organ_fund = OrganFund.objects.get(organization__id=organization_id)
        except OrganFund.DoesNotExist:
            return Response({'message': 'Organization funding details not found'}, 200)

        monthly_donations = Donation.objects.filter(fundme=organ_fund.fundme) \
            .annotate(month=TruncMonth('timestamp')) \
            .values('month') \
            .annotate(total_amount=Sum('amount')) \
            .order_by('-month')

        serializer = self.serializer_class(monthly_donations, many=True)

        return Response(serializer.data)



def chat_bot_ai(request):
    
    return render(request, 'chat_bot.html')