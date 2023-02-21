from rest_framework import serializers

from .models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

#after alot of research I think we may want to call the followers serializers in the views 
#and not in the serializer based on our current structure. 
class ProfileSerializer(serializers.ModelSerializer):
    username = UserSerializer(many=False)
    class Meta:
        model = Profile
        fields = ('id', 'username', 'email','bio','location','spotify_auth','follows')

