from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


User = get_user_model()

class EmailSender:
    @classmethod
    def send_email(cls, data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']],
        )
        email.content_subtype = 'html'
        email.send()

    @classmethod
    def organization_success(cls, organization):

        message = render_to_string('mails/organization_success.html', {'name':organization.name})
        data = {
            'email_subject': 'FUND | ME',
            'email_body': message,
            'to_email': organization.email
        }
        cls.send_email(data)

    @classmethod
    def donations_sucess(cls, user):
        context = {'user': user}

        message = render_to_string('mails/donations_sucess.html', context)
        data = {
            'email_subject': 'FUND | ME',
            'email_body': message,
            'to_email': user.email
        }
        cls.send_email(data)

    @classmethod
    def register_sucess(cls, user):
        context = {'user': user}

        message = render_to_string('mails/register_sucess.html', context)
        data = {
            'email_subject': 'FUND | ME',
            'email_body': message,
            'to_email': user.email
        }
        cls.send_email(data)
