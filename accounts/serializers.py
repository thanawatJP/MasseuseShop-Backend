from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

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
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "password", "first_name", "last_name"]

    def create(self, validated_data):
        # ใช้ set_password เพื่อ hash password
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            phone_number=validated_data.get("phone_number", ""),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
