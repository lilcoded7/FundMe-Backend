from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from fund.models.fundme import FundMe
from fund.models.category import Category
from fund.models.organizations import Organization, OrganizationCategory
from fund.models.donates import Donation

User = get_user_model()

class FundMeTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Education')
        self.organization_category = OrganizationCategory.objects.create(name='Non-profit')
        self.organization = Organization.objects.create(
            name='Test Organization', category=self.organization_category, is_active=True)
        self.fundme = FundMe.objects.create(
            title='Test FundMe', category=self.category, description='Test Description', organizer_name='Test Organizer', is_active=True)
        
    def test_list_fundme(self):
        url = reverse('fundme-list')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['fundme']), FundMe.objects.count())

    def test_retrieve_fundme(self):
        url = reverse('fundme-detail', kwargs={'pk': self.fundme.id})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.fundme.title)
        
    def test_create_fundme_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('fundme-create')  
        data = {
            'title': 'New FundMe',
            'category': self.category.id,
            'description': 'New Description',
            'organizer_name': 'New Organizer',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FundMe.objects.count(), 2)
        
    def test_create_fundme_unauthenticated(self):
        url = reverse('fundme-create')
        data = {
            'title': 'New FundMe',
            'category': self.category.id,
            'description': 'New Description',
            'organizer_name': 'New Organizer',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class OrganizationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.organization_category = OrganizationCategory.objects.create(name='Non-profit')
        self.organization = Organization.objects.create(
            name='Test Organization', category=self.organization_category, is_active=True)
        
    def test_list_organization_category(self):
        url = reverse('organization-category-list')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['org_category']), OrganizationCategory.objects.count())

    def test_retrieve_organization(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('organization-detail', kwargs={'pk': self.organization.id})  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.organization.name)
        
    def test_create_organization_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('organization-create')  
        data = {
            'name': 'New Organization',
            'category': self.organization_category.id,
            'email': 'new@organization.com',
            'phone': '123456789',
            'location': 'New Location'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Organization.objects.count(), 2)
        
    def test_create_organization_unauthenticated(self):
        url = reverse('organization-create') 
        data = {
            'name': 'New Organization',
            'category': self.organization_category.id,
            'email': 'new@organization.com',
            'phone': '123456789',
            'location': 'New Location'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DonationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Education')
        self.organization_category = OrganizationCategory.objects.create(name='Non-profit')
        self.organization = Organization.objects.create(
            name='Test Organization', category=self.organization_category, is_active=True)
        self.fundme = FundMe.objects.create(
            title='Test FundMe', category=self.category, description='Test Description', organizer_name='Test Organizer', is_active=True)
        
    def test_list_donations(self):
        url = reverse('donation-list')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['donations']), Donation.objects.count())

  
