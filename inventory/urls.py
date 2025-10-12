from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CategoryCreateView, CategoryDeleteView, CategoryDetailView,
                    CategoryListView, CategoryUpdateView,
                    InventoryChangeDetailView, InventoryChangeListCreateView,
                    InventoryCreateView, InventoryDeleteView,
                    InventoryDetailView, InventoryItemListView, InventoryUpdateView,
                    NotificationListView, PasswordChangeView, ProfileUpdateView, UserSupplierListView, SupplierCreateView, SupplierDeleteView, SupplierDetailView, SupplierUpdateView,
                    UserInventoryListView, InventoryReportView, UserListView, UserInfoView, UserRegistrationView, NotificationUpdateView, NotificationDeleteView)

urlpatterns = [
    # AUTHENTICATION
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('profile/', UserInfoView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),

    # CATEGORIES
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<str:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<str:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<str:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # INVENTORY ITEMS - FIXED ORDER
    path('inventory/user/', UserInventoryListView.as_view(), name='user_inventory_list'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory_item_create'),
    path('inventories/', InventoryItemListView.as_view(), name='inventory_item_list'),
    path('inventory/<str:pk>/', InventoryDetailView.as_view(), name='inventory_item_detail'),
    path('inventory/<str:pk>/update/', InventoryUpdateView.as_view(), name='inventory_item_update'),  
    path('inventory/<str:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_item_delete'),

    # SUPPLIERS - FIXED ORDER
    path('suppliers/', UserSupplierListView.as_view(), name='user_supplier_list'),
    path('supplier/create/', SupplierCreateView.as_view(), name='supplier_create'),
    path('supplier/<str:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),  # UNCOMMENTED
    path('supplier/<str:pk>/update/', SupplierUpdateView.as_view(), name='supplier_update'),
    path('supplier/<str:pk>/delete/', SupplierDeleteView.as_view(), name='supplier_delete'),

    # INVENTORY CHANGE
    path('inventory-changes/', InventoryChangeListCreateView.as_view(), name='inventory_changes_list'),
    path('inventory-changes/<str:pk>/', InventoryChangeDetailView.as_view(), name='inventory_change_detail'),

    # NOTIFICATIONS
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/<str:pk>/', NotificationUpdateView.as_view(), name='notification_update'),  # For PATCH
    path('notifications/<str:pk>/delete/', NotificationDeleteView.as_view(), name='notification_delete'),  # For DELETE
    path('inventory-report/', InventoryReportView.as_view(), name='inventory_report')
]