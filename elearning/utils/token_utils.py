# Standard Library imports
from datetime import datetime, timedelta
import jwt

# Core Django imports
import django.conf as settings

# Third-party imports
from rest_framework_simplejwt.tokens import RefreshToken

# App 


def manually_generate_auth_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# def generate_jwt_token(user, user_id):
#     # Set the expiration time for the token (e.g., 1 day from now)
#     expiration = datetime.utcnow() + timedelta(days=1)

#     # Create the payload containing user information
#     payload = {
#         'user_id': user_id,
#         'exp': expiration,
#     }

#     # Generate the JWT token using the secret key defined in Django settings
#     print(payload)
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#     JWT = JWTToken.objects.create(
#         token = token,
#         user = user
#     )

#     # Return the generated token as a string
#     return JWT