import datetime
import pytz
from django.conf import settings
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Expiring token for mobile and desktop clients.
    It expires every {n} hrs requiring client to supply valid username 
    and password for new one to be created.
    """
    # model = Token
    def authenticate_credentials(self, key):
        # models = self.get_model()
        try:
            # token = models.objects.select_related("user").get(key=key)
            token= Token.objects.get(key=key)
        except :
            raise AuthenticationFailed({"error": "Invalid or Inactive Token", "is_authenticated": False})

        if not token.user.is_active:
            raise AuthenticationFailed({"error": "Invalid user", "is_authenticated": False})
        utc_now = timezone.now()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - datetime.timedelta(minutes=1):
            raise AuthenticationFailed({"error": "Token has expired", "is_authenticated": False})
        return token.user, token