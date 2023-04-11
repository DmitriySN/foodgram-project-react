
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class CaseInsensitiveModelBackendEmail(ModelBackend):
    def authenticate(self, request, **kwargs):
        try:
            email = kwargs.get('email', None)
            if email is None:
                email = kwargs.get('username', None)
            user = User.objects.filter(email__iexact=email)[0]
            if user.check_password(kwargs.get('password', None)):
                return user
        except User.DoesNotExist:
            return None
        return None
