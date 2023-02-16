from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.urls import reverse
from cloudinary.models import CloudinaryField


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
    is_archived = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username

class Image(models.Model):
    # image = models.ImageField(upload_to='images/', blank=True, null=True)
    image = CloudinaryField('image')
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Journal(models.Model):
    '''
    default privacy: 0 - private; 1 - followers; 2 - public
    '''

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
    is_archived = models.BooleanField(default=False)

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
    is_archived = models.BooleanField(default=False)

    @property
    def get_html_url(self):
        url = reverse('core:entry_landing', args=(self.id,))
        return url

    
    def _str_(self):
            return(
                f"{self.journal.user.username}"
                f"{self.title}"
                f"({self.created_at:%Y-%m-%d %H:%M}:"
            )

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name="user_comments", on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry,related_name="entry_comments", on_delete=models.CASCADE, null=True)
    journal = models.ForeignKey(Journal,related_name="journal_comments", on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_replies')
    is_archived = models.BooleanField(default=False)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_at').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

class Like(models.Model):
    like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,related_name="user_likes", on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry,related_name="entry_likes", on_delete=models.CASCADE, null=True)
    journal = models.ForeignKey(Journal,related_name="journal_likes", on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, related_name="comment_likes", on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, related_name="image_likes", on_delete=models.CASCADE, null=True)
    #add videos when videos. 

class Song(models.Model):
    source_url = models.CharField(max_length=1000)
    entry = models.ForeignKey(Entry,related_name="entry_song", on_delete=models.CASCADE, null=True)
    journal = models.ForeignKey(Entry,related_name="journal_song", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)

class Video(models.Model):
    source_url = models.CharField(max_length=1000)
    entry = models.ForeignKey(Entry,related_name="entry_videos", on_delete=models.CASCADE, null=True)
    journal = models.ForeignKey(Entry,related_name="journal_videos", on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    is_archived = models.BooleanField(default=False)
