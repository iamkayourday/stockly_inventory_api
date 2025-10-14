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
                          InventoryItemSerializer, InventoryItemUpdateSerializer, NotificationSerializer, PasswordChangeSerializer, ProfileSerializer,
                          UserListSerializer, UserRegistrationSerializer, SupplierSerializer)


#1. USER MODELS VIEWS

#1.1 This view allows new user registration
class UserRegistrationView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

#1.2 This view lists all users, accessible only by admin users
class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

#1.3 This view allows users to retrieve and update their own information
class UserInfoView(RetrieveUpdateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

#1.4 Profile views to Retrieve and Update Profile
class ProfileUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

#1.5 Password Change View
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
        
        # Keeps user logged in after password change
        update_session_auth_hash(request, user)
        
        return Response({"message": "Password updated successfully."})


#2. CATEGORY MODEL VIEWS(create, Update and Delete by admin only)

#2.1 List Categories
class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'created_at', 'updated_at']

#2.2 Create Category
class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

#2.3 Retrieve Category
class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

#2.4 Update Category
class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

#2.5 Delete Category
class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


#3. INVENTORY ITEM VIEWS

#3.1 List inventory Items(Admin users see all items, regular users see their own items only)
class InventoryItemListView(ListAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAdminUser]
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

#3.2 Create inventory Item
class InventoryCreateView(CreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#3.3 Retrieve inventory Item
class InventoryDetailView(RetrieveAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)

#3.4 Update inventory Item
class InventoryUpdateView(UpdateAPIView):
    serializer_class = InventoryItemUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)

#3.5 Delete inventory Item
class InventoryDeleteView(DestroyAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user)
    
#3.6 User Inventory List View
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


#4. INVENTORY CHANGE VIEWS

#4.1 List and Create Inventory Changes
class InventoryChangeListCreateView(ListCreateAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['change_type', 'change_date', 'item__name', 'user__username']
    search_fields = ['item__name', 'reason', 'user__username']
    ordering_fields = ['change_date', 'change_type', 'quantity_change']
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user).select_related('item', 'user')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
#4.2 Retrieve Inventory Change Details
class InventoryChangeDetailView(RetrieveAPIView):
    serializer_class = InventoryChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryChange.objects.filter(item__user=self.request.user)

# Update and Delete Inventory Change (if needed, usually changes are not updated or deleted)
# I don't recommend allowing updates or deletions of inventory changes for audit purposes
# class InventoryChangeUpdateView(UpdateAPIView):
#     serializer_class = InventoryChangeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return InventoryChange.objects.filter(item__user=self.request.user)
    
# class InventoryChangeDeleteView(DestroyAPIView):
#     serializer_class = InventoryChangeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return InventoryChange.objects.filter(item__user=self.request.user)
    

#5. SUPPLIER VIEWS

#5.1 Create Supplier
class SupplierCreateView(CreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#5.2 List Suppliers
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

#5.3 Retrieve Supplier Details
class SupplierDetailView(RetrieveAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)

#5.4 Update Supplier Details
class SupplierUpdateView(UpdateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)

#5.5 Delete Supplier
class SupplierDeleteView(DestroyAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(user=self.request.user)


#6. NOTIFICATION VIEWS

#6.1 Notification List View
class NotificationListView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

#6.2 Notification Update View (e.g., mark as read)
class NotificationUpdateView(UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

#6.3 Notification Delete View
class NotificationDeleteView(DestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


#7. INVENTORY REPORT VIEW
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