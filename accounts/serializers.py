from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # custom claims
        token["username"] = user.username
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["roles"] = list(user.groups.values_list("name", flat=True))

        return token
