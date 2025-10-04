from django.contrib.auth import update_session_auth_hash
from rest_framework import status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, ListCreateAPIView
from .serializers import UserRegistrationSerializer, UserListSerializer, PasswordChangeSerializer, CategorySerializer, InventoryItemSerializer, InventoryChangeSerializer
from .models import CustomUser, Category, InventoryItem,InventoryChange

# Create your views here.
# This view handles user registration
class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


# This view lists all users, accessible only by admin users
class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]


class PasswordChangeView(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = self.get_object()
        
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"old_password": ["Wrong password."]}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Keep user logged in after password change
        update_session_auth_hash(request, user)
        
        return Response({"message": "Password updated successfully."})


# Category views will go here to Add, List, Update, Retrieve, Delete Categories

# List Categories
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'created_at', 'updated_at']

# Create Category
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Retrieve Category
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Update Category
class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Delete Category
class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

# Inventory Item views will go here to Add, List, Update, Retrieve, Delete Inventory Items

# List inventory Items
class InventoryItemListView(ListAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'price', 'quantity', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'quantity', 'created_at', 'updated_at']
    ordering = ['-updated_at']

class InventoryCreateView(CreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InventoryDetailView(RetrieveAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class InventoryUpdateView(UpdateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    read_only_fields = ['quantity']

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)

class InventoryDeleteView(DestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)
    
# User Inventory List View
class UserInventoryListView(ListAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'price', 'quantity', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'category__name']

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)

# Inventory Change views will go here to Add, List, Update, Retrieve, Delete Inventory Changes
class InventoryChangeListCreateView(ListCreateAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users only see changes for their own items
        return InventoryChange.objects.filter(item__user=self.request.user).select_related('item', 'user')
    
    def perform_create(self, serializer):
        # User is auto-set, quantities auto-calculated in model save()
        serializer.save(user=self.request.user)
    
class InventoryChangeDetailView(RetrieveAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user)