from django.shortcuts import render
from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer, StaffSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .models import CustomUser

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

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        print("Refresh token from cookie:", refresh_token)

        if not refresh_token:
            return Response({"detail": "No refresh token in cookie"}, status=status.HTTP_400_BAD_REQUEST)

        # inject token เข้าไปใน request.data ให้ SimpleJWT ใช้ได้
        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            new_access = response.data.get("access")
            response.set_cookie(
                key="access_token",
                value=new_access,
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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.is_staff:
            staff_data = getattr(user, "staff_data", None)
            staff_info = {
                "expertise": getattr(staff_data, "expertise", None),
                "hire_date": getattr(staff_data, "hire_date", None),
                "salary": getattr(staff_data, "salary", None),
            }
            return Response({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "image_url": user.image_url,
                "is_staff": user.is_staff,
                **staff_info
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "image_url": user.image_url,
            }, status=status.HTTP_200_OK)
        
    def put(self, request):
        user = request.user
        data = request.data

        serializer = ProfileSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.update(user, serializer.validated_data)

            # Update Staff_Data if exists
            if hasattr(user, "staff_data"):
                staff_data = user.staff_data
                staff_data.expertise = data.get("expertise", staff_data.expertise)
                # ถ้าอยากให้ update hire_date หรือ salary ก็ทำตรงนี้ได้
                staff_data.save()

            return Response({
                "message": "Profile updated successfully",
                "user": {
                    "id": updated_user.id,
                    "first_name": updated_user.first_name,
                    "last_name": updated_user.last_name,
                    "username": updated_user.username,
                    "email": updated_user.email,
                    "phone_number": updated_user.phone_number,
                    "expertise": getattr(updated_user.staff_data, "expertise", None) if hasattr(user, "staff_data") else None,
                }
            }, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone_number": user.phone_number,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddStaffView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        staff_users = CustomUser.objects.filter(is_staff=True)
        serializer = StaffSerializer(staff_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StaffSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Staff created successfully",
                "user": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "phone_number": user.phone_number,
                    "salary": user.staff_data.salary,
                    "expertise": user.staff_data.expertise,
                    "hire_date": user.staff_data.hire_date,
                    "is_staff": True,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        user_id = request.data.get("id")
        try:
            user = CustomUser.objects.get(id=user_id, is_staff=True)
        except CustomUser.DoesNotExist:
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StaffSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.update(user, serializer.validated_data)

            # Update Staff_Data
            staff_data = updated_user.staff_data
            staff_data.expertise = request.data.get("expertise", staff_data.expertise)
            staff_data.salary = request.data.get("salary", staff_data.salary)
            # ถ้าอยากให้ update hire_date ก็ทำตรงนี้ได้
            staff_data.save()

            return Response({
                "message": "Staff updated successfully",
                "user": {
                    "id": updated_user.id,
                    "first_name": updated_user.first_name,
                    "last_name": updated_user.last_name,
                    "username": updated_user.username,
                    "email": updated_user.email,
                    "phone_number": updated_user.phone_number,
                    "expertise": staff_data.expertise,
                    "salary": staff_data.salary,
                }
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user_id = request.data.get("user_id")
        try:
            user = CustomUser.objects.get(id=user_id, is_staff=True)
            user.delete()
            return Response({"message": "Staff deleted successfully"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)
