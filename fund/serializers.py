from rest_framework import serializers
from fund.models.fundme import FundMe
from fund.models.fundimages import Fundimage
from fund.models.donates import Donation
from fund.models.comments import CommentReaction


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