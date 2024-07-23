from rest_framework import serializers
from fund.models.fundme import FundMe
from fund.models.fundimages import Fundimage
from fund.models.donates import Donation
from fund.models.comments import CommentReaction
from fund.models.organizations import Organization, BankAccount
from fund.models.sponsorships import Sponsorship
from accounts.serializers import UserSerializer
from fund.models.category import Category
from fund.models.organizations import OrganizationCategory
from fund.models.transactions import Transactions
from fund.models.company import Company



class FundMeSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = FundMe
        fields = '__all__'

    def get_image(self, obj):
        request = self.context.get('request')
        
        # Handle queryset (many=True) and single instance cases
        if isinstance(obj, list):
            return [self.build_absolute_image_url(item, request) for item in obj]
        return self.build_absolute_image_url(obj, request) if obj else None

    def build_absolute_image_url(self, obj, request):
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'



class OrganizationsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationCategory
        fields = '__all__'


class FundImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundimage
        fields = '__all__'


class DonationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        fields = ['amount']
    


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CommentReaction
        fields = ['message']


class CommentsSerializer(serializers.ModelSerializer):
    fundme = FundMeSerializer()
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
        exclude = ['is_active']



class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'



class TransactionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transactions
        exclude = ['trans_id']



class DonationsSerializer(serializers.ModelSerializer):
    fundme = FundMeSerializer()
    class Meta:
        model = Donation
        fields = '__all__'



class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'