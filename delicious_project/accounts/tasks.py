from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from delicious_project import settings

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
