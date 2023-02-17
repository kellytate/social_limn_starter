from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Journal, Entry, Image, Comment, Like, Song, Place

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    
    fields = ["username", "is_active"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
admin.site.register(Journal)
admin.site.register(Entry)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Song)
admin.site.register(Place)

