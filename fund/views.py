from django.shortcuts import render, get_object_or_404
from fund.models.fundme import FundMe
from fund.models.category import Category
from fund.models.volunteers import Volunteer
from fund.serializers import * 
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


# Create your views here.


class FundMeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    serializer_class = FundMeSerializer
    permission_classes  = [AllowAny]
    queryset = FundMe.objects.all()

  