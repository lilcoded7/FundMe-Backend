from django.shortcuts import render, get_object_or_404
from fund.models.fundme import FundMe
from fund.serializers import * 
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from fund.models.fundimages import Fundimage
from fund.models.comments import CommentReaction
from fund.models.sponsorships import Sponsorship
from setup.permissions import IsApexAdmin
from fund.notifications import EmailSender


# Create your views here.


class FundMeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = FundMeSerializer
    permission_classes  = [AllowAny]
    queryset = FundMe.objects.all()

class CreateFundMeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = FundMeSerializer
    permission_classes  = [IsAuthenticated]
    queryset = FundMe.objects.all()

class SponsorshipViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = SponsorshipSerializer
    permission_classes  = [AllowAny]
    queryset = Sponsorship.objects.all()


class FundImagesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = FundImagesSerializer
    permission_classes  = [AllowAny]
    queryset = Fundimage.objects.all()


class ListOrRetreiveDonerDonationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = DonerDonationFundMe
    permission_classes  = [AllowAny]
    queryset = Donation.objects.all()


class CommentViewSet(viewsets.ViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_username(self, request):
        if request.user.is_authenticated:
            username = request.user.username
            profile = request.user.profile  
        else:
            username = 'Anonymous'
            profile = None
        return username, profile

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username, profile = self.get_username(request)
            serializer.validated_data['username'] = username
            serializer.validated_data['profile'] = profile
            serializer.save()
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
        return Response({'organization':Organization(organization, many=True)})
        

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Your Request Has Been Received, We Are Currently viewing Your Request'}, 200)
        return Response({'messages':serializer.errors}, 400)
    

class ListUpdateDeleteOrganizationViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = Organization
    permission_classes  = [IsApexAdmin]
    queryset = Organization.objects.all()