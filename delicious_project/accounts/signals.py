from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from delicious_project.accounts.models import Profile, DeliciousAppUser


@receiver(post_delete, sender=Profile)
def delete_user(instance, **kwargs):
    instance.user.delete()


@receiver(post_save, sender=DeliciousAppUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Users'))
