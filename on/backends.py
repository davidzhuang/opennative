from django.conf import settings
from django.contrib.auth.models import User, check_password
from django.contrib.auth.backends import ModelBackend
from django.core.validators import email_re

class EmailAuthBackend(ModelBackend):

    def authenticate(self, username=None, password=None):
        try:
            if email_re.search(username):
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 
        return None 

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
