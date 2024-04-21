from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.exceptions import NotFound

from rest_framework.response import Response
from rest_framework import serializers, permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from accounts.models import *
from accounts.serializers import *
from rest_framework import filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user
from rest_framework.fields import empty
from .pagination import CustomPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from django.contrib.auth import login,  logout, authenticate
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication

class RegisterUser(ListCreateAPIView): #Register User
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        for user in User.objects.all():
            if user:
                Token.objects.get_or_create(user=user)
        return User.objects.none()

class LoginView(ListAPIView):
    queryset = User.objects.none()
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        print("logged in", user.username)
        if user.is_authenticated:
            print("Authenticated")
            token = Token.objects.get_or_create(user=user)[0].key
            return Response({"token": token})
        return Response(None)


class UserProfileView(RetrieveAPIView): #Shows details of a user profile
    serializer_class = UserProfileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_object(self):
        return get_object_or_404(UserModel, id=self.request.user.id)


class UserProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_object(self):
        return get_object_or_404(UserModel, id=self.request.user.id)



from rest_framework.decorators import api_view, permission_classes

@api_view(["POST"])
def user_logout(request):
    #request.user.auth_token.delete()
    logout(request)
    return Response('Logged Out')



@api_view(['POST'])
def login_user(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = authenticate(request, username =username, password=password)
    print("user is", user)
    if user.is_authenticated:
        print("YAY")
    if user is not None:
        return Response({"Logged in"})
    return Response({"message": "Invalid credentials"}, status=404)