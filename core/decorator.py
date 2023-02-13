from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect



# def is_follower_of_user(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     A decorator to check logged in user is a follower of profile
#     '''

#     actual_decorator = user_passes_test(

#         lambda u: u.is_active and u.is_authenticated and u in journal.user.follows
#     )

# def owner_only(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

#     actual_decorator = user_passes_test(
        
#         lambda u: u.is_active and u.is_authencated and 
#     )

# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

#     model = cls.query.get(model_id)

#     if not model:
#         abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))

#     return model

# def validate_perm(cls, request):

#     if request.user != cls.user:
#         return(redirect(f"core:{cls}._profile", pk=cls.pk))


