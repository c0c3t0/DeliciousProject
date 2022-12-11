import os

from celery import shared_task
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from delicious_project import settings
from delicious_project.accounts.tokens import account_activation_token

UserModel = get_user_model()


@shared_task
def send_successful_registration_email(user_pk):
    user = UserModel.objects.get(pk=user_pk)
    subject = 'Thank you for your registration'
    message = 'Your account has been created and a verification email has been sent to your email. ' \
              'Please click on the verification link included in the email to activate your account.'

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        (user.email,),
    )


@shared_task
def confirm_email(user_pk):
    user = UserModel.objects.get(pk=user_pk)

    subject = 'Activate Your Account'
    message = render_to_string('auth/confirm_email.html', {
        'user': user,
        'domain': os.environ.get('ALLOWED_HOSTS'),
        'port': ':8000',
        'uid': urlsafe_base64_encode(force_bytes(user_pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
    )

