import random
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404


def get_5_random_nums() -> int:
    return random.randint(10000, 99999)


def get_user_ip_address(request):
    user_ip_address = request.META.get("HTTP_X_FORWARDED_FOR")
    if user_ip_address:
        ip = user_ip_address.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip



class EmailSender:
    def send_email(self, data):
        email = EmailMessage(
            subject    = data['email_subject'],
            body       = data['email_body'],
            to         = [data['to_email']],
        )
        email.content_subtype = 'html'
        email.send()


    def send_email_success_message(self, user):
        context = {'user':user}
        message = render_to_string('mails/register_success.html', context)
        data = {
            'email_subject':'Fund Me',
            'email_body': message,
            'to_email':user.email
            }
        self.send_email(data)


    def send_fundme_create_success(self, user):
        context = {'user':user}
        message = render_to_string('mails/fundme_success.html', context)
        data = {
            'email_subject':'Fund | Me',
            'email_body': message,
            'to_email':user.email
            }
        self.send_email(data)


    def send_create_organization_success(self, user):
        message = render_to_string('mails/organization_success.html', user)
        data = {
            'email_subject':'Fund | Me',
            'email_body': message,
            'to_email':user.email
            }
        self.send_email(data)
    
    def send_organization_approved_success(self, user):
        message = render_to_string('mails/organization_approved_success.html', user)
        data = {
            'email_subject':'Fund | Me',
            'email_body': message,
            'to_email':user.email
            }
        self.send_email(data)
