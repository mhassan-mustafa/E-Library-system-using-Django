from django.contrib.auth.backends import ModelBackend
from .models import Members

class MembersBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Members.objects.get(email=email)
        except Members.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def get_user(self, user_id):
        try:
            return Members.objects.get(pk=user_id)
        except Members.DoesNotExist:
            return None
