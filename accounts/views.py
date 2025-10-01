from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "roles": list(user.groups.values_list("name", flat=True)),
        })

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            data = response.data
            access_token = data.get("access")
            refresh_token = data.get("refresh")

            # set cookie
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,
                samesite="Lax"
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite="Lax"
            )

        return response
    
class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=200)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
