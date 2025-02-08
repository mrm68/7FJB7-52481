# accounts/urls.py
from django.urls import path
from .views import UserRegistrationView, CustomLogoutView

urlpatterns = [
    path('logout/', CustomLogoutView.as_view(), name='custom-logout'),
    path('signup/', UserRegistrationView.as_view(), name='user_signup'),
]
