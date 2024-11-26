from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from users.models import Users

@receiver(post_save, sender=User)
def create_or_update_users(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(
            user=instance,
            username=instance.username,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )
    else:
        user_profile = Users.objects.filter(user=instance).first()
        if user_profile:
            user_profile.username = instance.username
            user_profile.first_name = instance.first_name
            user_profile.last_name = instance.last_name
            user_profile.email = instance.email
            user_profile.save()
