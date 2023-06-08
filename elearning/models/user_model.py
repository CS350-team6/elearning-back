# # Standard Library imports

# # Core Django imports
# from django.db import models
# from django.db import transaction
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.utils import timezone

# # Third-party imports

# # App imports

# class UserManager(BaseUserManager):
#     def create_user(self, username, email_address, password=None):
#         """If you don't verify your primary email address, your account will get deleted
#         if another user attempts to create an account with that email address."""
#         user_model = self.model(username=username, email_address=email_address)
#         user_model.set_password(password)

#         return user_model

#     def create_superuser(self, username, email_address, password=None):
#         with transaction.atomic():
#             username = username
#             user_model = self.create_user(username, email_address, password)
#             user_model.is_admin = True
#             user_model.is_staff = True
#             user_model.save()
#         return user_model

# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=15, unique=True)
#     email_address = models.EmailField(unique=True)
#     date_joined = models.DateTimeField(default=timezone.now)

#     # These three fields are required by `AbstractBaseUser`
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = "username"
#     EMAIL_FIELD = "email_address"
#     REQUIRED_FIELDS = ["email_address"]

#     def __str__(self):
#         return self.username

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, fwdeveryone):
#         return True