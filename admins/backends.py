from django.contrib.auth.backends import ModelBackend
from .models import Admins

class AdminsBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Admins.objects.get(username=username)
        except Admins.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            return Admins.objects.get(pk=user_id)
        except Admins.DoesNotExist:
            return None
