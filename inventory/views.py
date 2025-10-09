from django.contrib.auth import update_session_auth_hash
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, CustomUser, InventoryChange, InventoryItem, Notification, Supplier
from .serializers import (CategorySerializer, InventoryChangeSerializer,
                          InventoryItemSerializer, NotificationSerializer, PasswordChangeSerializer, ProfileSerializer,
                          UserListSerializer, UserRegistrationSerializer, SupplierSerializer)


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

class UserInfoView(RetrieveUpdateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class ProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



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

    # def get_queryset(self):
    #     return Category.objects.filter(user=self.request.user).order_by('-updated_at')

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
    # permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'category', 'price', 'quantity', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'category__name', 'supplier', 'barcode']
    ordering_fields = ['name', 'price', 'quantity', 'created_at', 'updated_at']
    ordering = ['-updated_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Low stock filter
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None:
            if low_stock.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))
        
        return queryset


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
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = InventoryItem.objects.filter(user=self.request.user)

        # Low stock filter
        low_stock = self.request.query_params.get('low_stock', None)
        if low_stock is not None:
            if low_stock.lower() in ['true', '1', 'yes']:
                queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))

        return queryset


# Inventory Change views will go here to Add, List, Update, Retrieve, Delete Inventory Changes
class InventoryChangeListCreateView(ListCreateAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user).select_related('item', 'user')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    
class InventoryChangeDetailView(RetrieveAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user)
    
class InventoryChangeUpdateView(UpdateAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user)
    
class InventoryChangeDeleteView(DestroyAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user)
    

# Supplier views will go here to Add, List, Update, Retrieve, Delete Suppliers
class SupplierCreateView(CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserSupplierListView(ListAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'contact_person', 'email', 'phone_number', 'city', 'state', 'country', 'created_at', 'updated_at']
    search_fields = ['name', 'contact_person', 'email', 'phone_number']
    ordering_fields = ['name', 'created_at', 'updated_at']
    ordering = ['-updated_at']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)
    
class SupplierDetailView(RetrieveAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)
    
class SupplierUpdateView(UpdateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)

class SupplierDeleteView(DestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)

class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
class InventoryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        items = InventoryItem.objects.filter(user=user)
        changes = InventoryChange.objects.filter(user=user).order_by('-change_date')

        total_value = sum(item.quantity * item.price for item in items)
        low_stock = items.filter(quantity__lte=F('low_stock_threshold'))

        report = {
            "total_inventory_value": total_value,
            "total_items_in_stock": items.count(),
            "low_stock_items": [item.name for item in low_stock],
            "stock_levels": [
                {
                    "name": item.name,
                    "category": item.category.name,
                    "quantity": item.quantity,
                    "unit_price": item.price,
                    "total_value": item.quantity * item.price
                } for item in items
            ],
            "change_history": [
                {
                    "date": change.change_date,
                    "item": change.item.name,
                    "type": change.change_type,
                    "quantity": change.quantity_change,
                    "from": change.previous_quantity,
                    "to": change.new_quantity,
                    "reason": change.reason
                } for change in changes
            ]
        }

        return Response(report)