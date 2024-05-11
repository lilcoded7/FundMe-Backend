from rest_framework import serializers
from fund.models.fundme import FundMe
from fund.models.fundimages import Fundimage


class FundMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundMe
        fields = '__all__'


class FundImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundimage
        fields = '__all__'