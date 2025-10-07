from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (CategoryCreateView, CategoryDeleteView, CategoryDetailView,
                    CategoryListView, CategoryUpdateView,
                    InventoryChangeDetailView, InventoryChangeListCreateView,
                    InventoryCreateView, InventoryDeleteView,
                    InventoryDetailView, InventoryItemListView,
                    InventoryUpdateView, PasswordChangeView,
                    UserInventoryListView, UserListView, UserRegistrationView)

urlpatterns = [
    # AUTHENTICATION
    path('register/', UserRegistrationView.as_view(), name='user_registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('users/', UserListView.as_view(), name='user_list'),

    # CATEGORIES
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # INVENTORY ITEMS
    path('inventories/', InventoryItemListView.as_view(), name='inventory_item_list'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory_item_create'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory_item_detail'),
    # path('inventory/<int:pk>/update/', InventoryUpdateView.as_view(), name='inventory_item_update'),
    path('inventory/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_item_delete'),
    path('inventory/user/', UserInventoryListView.as_view(), name='user_inventory_list'),

    # INVENTORY CHANGE
    path('inventory-changes/', InventoryChangeListCreateView.as_view(), name='inventory_changes_list'),
    path('inventory-changes/<str:pk>/', InventoryChangeDetailView.as_view(), name='inventory_change_detail'),

]
