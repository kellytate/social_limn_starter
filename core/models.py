from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


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
    profile_img = models.ImageField(upload_to='images/', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    spotify_auth = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return self.user.username

class Image(models.Model):
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Journal(models.Model):
    user = models.ForeignKey(User,
    related_name="user_journals",
    on_delete=models.DO_NOTHING) 
    title = models.CharField(max_length=200)
    metaTitle = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    cover_img = models.ImageField(upload_to='images/')
    default_privacy = models.IntegerField(default=0)
    is_liked = models.BooleanField(default=False)

    def _str_(self):
        return(
            f"{self.user}"
            f"{self.title}"
            f"({self.created_at:%Y-%m-%d %H:%M}:"
        )

class Entry(models.Model):
    journal = models.ForeignKey(Journal,
    related_name="journal_entries",
    on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    body= models.CharField(max_length=2000)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    entry_privacy = models.IntegerField(default=0)
    image = models.ManyToManyField('Image',blank=True)

    def _str_(self):
            return(
                f"{self.journal.user.username}"
                f"{self.title}"
                f"({self.created_at:%Y-%m-%d %H:%M}:"
            )