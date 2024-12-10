from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from accounts.serializers import SignupSerializer, LoginSerializer, ProfileSerializer
from accounts.models import Profile
from accounts.permissions import IsOwnerProfile


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"회원가입에 성공하였습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            auth_login(request, user)
            return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_logout(request)
        return Response({"message": "로그아웃"}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerProfile]

    def get_object(self):
        try:
            profile =  Profile.objects.get(user=self.request.user)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise NotFound({"detail": "Profile not found."})
        
    def get(self, request):
        profile = self.get_object()
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        profile = self.get_object()

        serializer = ProfileSerializer(profile, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)