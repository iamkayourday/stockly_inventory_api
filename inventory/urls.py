from django.urls import path
from .views import UserRegistrationView, UserListView, PasswordChangeView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('users/', UserListView.as_view(), name='user_list'),
]
