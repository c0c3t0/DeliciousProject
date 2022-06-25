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


'''ocess] Task delicious_project.accounts.tasks.send_successful_registration_email[449ad2f3-17f8-4546-8d00-fc783a17799b] received
[2022-06-25 20:26:27,897: INFO/ForkPoolWorker-1] Task delicious_project.accounts.tasks.send_successful_registration_email[
449ad2f3-17f8-4546-8d00-fc783a17799b] succeeded in 35.15729672700036s: None
'''