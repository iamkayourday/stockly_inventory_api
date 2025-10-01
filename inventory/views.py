from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from .serializers import UserRegistrationSerializer
from .models import CustomUser

# Create your views here.
# This view handles user registration
class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


