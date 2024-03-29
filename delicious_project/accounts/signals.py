from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from delicious_project.accounts.models import Profile
from delicious_project.accounts.tasks import send_successful_registration_email, confirm_email

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def user_created(instance, created, *args, **kwargs):
    if not created:
        return

    send_successful_registration_email.delay(instance.pk)
    confirm_email.delay(instance.pk)

@receiver(post_delete, sender=Profile)
def delete_user_and_profile(instance, *args, **kwargs):
    user = instance.user
    user.delete()
