from django.urls import path
from . import views
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView
app_name="accounts"



urlpatterns = [
    path('register/', views.RegisterUser.as_view()),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout),
    path('profile/',views.UserProfileView.as_view()),
    path('updateProfile/', views.UserProfileUpdateView.as_view()),
]