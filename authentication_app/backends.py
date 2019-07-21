from authentication_app.models import User

class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate( username=None, password=None):
        """
        Authentication method
        """
        
        try:
            user = User.objects.get(email=username)
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
