from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# The creation of this User model and profile uses a post_save/Signal to create
# the profile as soon as a user is saved. If there are strange errors, check that
# this feature is working properly.

User = get_user_model()

# Create a profile for each user. This is done with the receiver decorator
# post_save.connect(create_profile, sender=User)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    email = models.EmailField(blank=False)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    spotify_auth = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
