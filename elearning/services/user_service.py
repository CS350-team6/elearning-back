# # Standard Library imports

# # Core Django imports
# from django.forms.models import model_to_dict
# from django.db import transaction

# # Third-party imports

# # App imports
# from ..models.user_model import User
# from ..utils import token_utils

# def create_user_account(username, email_address, password):
#     if User.objects.filter(username=username, email_address=email_address).exists():
#         raise Exception("An account with this username and email address already exists!")

#     with transaction.atomic():
#         user_model = User.objects.create_user(
#             username=username,
#             email_address=email_address,
#             password=password,
#         )
#         user_model.full_clean()
#         user_model.save()

#     # Return an auth token so that the front end doesn't need to do another round trip to log in the user.
#     auth_token = token_utils.manually_generate_auth_token(user_model)

#     return ( user_model, auth_token, )


# def get_user_profile_from_user_model(user_model):
#     user_model_dict = model_to_dict(user_model)

#     user_model_dict['date_joined'] = user_model_dict['date_joined'].isoformat()

#     allowlisted_keys = ['username', 'email_address', 'date_joined']

#     for key in list(user_model_dict.keys()):
#         if not key in allowlisted_keys:
#             user_model_dict.pop(key)

#     return user_model_dict