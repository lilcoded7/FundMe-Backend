from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from fund.notifications import EmailSender
from fund.models.organizations import Organization
from fund.models.donates import Donation
from fund.models.fundme import FundMe



User = get_user_model()

@receiver(post_save, sender=Organization)
def organization_success(sender, instance, created, **kwargs):
    if created:
        EmailSender.organization_success(instance.email)


