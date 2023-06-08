# Standard Library imports

# Core Django imports

# Third-party imports
from factory.django import DjangoModelFactory

# App imports
from ..services import user_service
from ..models.user_model import *


class UserFactory(DjangoModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        username = kwargs.pop("username")
        email_address = kwargs.pop("email_address")
        password = kwargs.pop("password", "1234567a")

        user_model, _ = user_service.create_user_account(username, email_address, password)

        if kwargs:
            for kwarg, value in kwargs.items():
                setattr(user_model, kwarg, value)

            user_model.save()

        return user_model

    class Meta:
        model = User
