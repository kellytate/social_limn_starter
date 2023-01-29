from rest_framework import serializers

from .models import Profile, User


class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model = User
        #will add a user link and profile pic to these later. 
        feilds = ('username')

#after alot of reserch I think we may want to call the followers seralizers in the views 
#and not in the seralizer based on our current structure. 
class ProfileSeralizer(serializers.ModelSerializer):
    username = UserSeralizer(many=False)
    class Meta:
        model = Profile
        feilds = ('id', 'username', 'email','bio','location','spotify_auth','follows')

