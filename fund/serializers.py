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
from fund.models.sliders import Slider

class WithdrawalSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=11, decimal_places=2)

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount cannot be less than 0.")
        return value


class TransactionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Transactions
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

class OrganizationCreateFundMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundMe
        exclude = ['raised', 'status']



class FundMeSerializer(serializers.ModelSerializer):
    fund_image = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = FundMe
        fields = '__all__'

    def get_fund_image(self, obj):  
        request = self.context.get('request')
        
        if isinstance(obj, list):
            return [self.build_absolute_image_url(item, request) for item in obj]
        return self.build_absolute_image_url(obj, request) if obj else None

    def build_absolute_image_url(self, obj, request):
        if obj.fund_image:
            return request.build_absolute_uri(obj.fund_image.url)
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

    
class DonationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        fields = ['donor_fullname', 'amount', 'fundme', 'timestamp']



class SliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'
    


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


class CreateOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ['balance', 'is_active']


class OrganizationSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()
    cert = serializers.SerializerMethodField()
    category = OrganizationsCategorySerializer()

    class Meta:
        model = Organization
        fields = '__all__'

    def get_logo(self, obj):
        if obj.logo:
            return self.context['request'].build_absolute_uri(obj.logo.url)
        return None

    def get_cert(self, obj):
        if obj.cert:
            return self.context['request'].build_absolute_uri(obj.cert.url)
        return None




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