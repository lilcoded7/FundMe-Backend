from django.shortcuts import render, get_object_or_404
from fund.models.fundme import FundMe
from fund.serializers import * 
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from fund.models.fundimages import Fundimage
from fund.models.comments import CommentReaction


# Create your views here.


class FundMeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = FundMeSerializer
    permission_classes  = [AllowAny]
    queryset = FundMe.objects.all()

class CreateFundMeViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = FundMeSerializer
    permission_classes  = [IsAuthenticated]
    queryset = FundMe.objects.all()


class FundImagesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = FundImagesSerializer
    permission_classes  = [AllowAny]
    queryset = Fundimage.objects.all()


class DonerDonationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
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

    def post(self, request, fundme_id):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            fundme = get_object_or_404(FundMe, id=fundme_id)
            serializer.validated_data['fundme'] = fundme
            serializer.save()
            return Response({'message': 'Amount Donated Successfully'}, status=200)
        return Response({'message': serializer.errors}, status=400)