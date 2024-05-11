from rest_framework import serializers
from fund.models.fundme import FundMe


class FundMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundMe
        fields = '__all__'
