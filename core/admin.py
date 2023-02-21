from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Journal, Entry, Image, Comment, Like, Song, Place, Video


class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    
    fields = ["username", "is_active"]
    inlines = [ProfileInline]

class EntryAdmin(admin.ModelAdmin):
    list_display = ('journal' , 'title', 'body','location' ,'created_at','updated_at', 'entry_privacy','is_archived')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Journal)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Song)
admin.site.register(Place)
admin.site.register(Video)

