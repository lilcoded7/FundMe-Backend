from rest_framework import serializers
from fund.models.fundme import FundMe
from fund.models.fundimages import Fundimage
from fund.models.donates import Donation
from fund.models.comments import CommentReaction
from fund.models.organizations import Organization
from fund.models.sponsorships import Sponsorship
from accounts.serializers import UserSerializer


class FundMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundMe
        fields = '__all__'


class FundImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundimage
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        fields = ['donor_fullname', 'amount']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReaction
        fields = '__all__'


class DonerDonationFundMe(serializers.ModelSerializer):
    fundme =  FundMeSerializer()
    
    class Meta:
        model = Donation
        fields = '__all__'


class SponsorshipSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sponsorship
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Organization
        exclude = ['fundme']


















