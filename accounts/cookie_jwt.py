from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except ValidationError:
            return None 

        return self.get_user(validated_token), validated_token
