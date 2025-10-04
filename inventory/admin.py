from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Category, InventoryItem

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['id', 'email', 'username', 'first_name', 'middle_name', 'last_name', 'phone_number', 'is_staff', 'is_active', 'last_login', 'date_joined',
    ]

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'phone_number', 'first_name', 'middle_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'phone_number', 'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email', 'username', 'phone_number')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user', 'company_name', 'address', 'website', 'city', 'state', 'country', 'postal_code',  'tax_id', 'business_type','about','logo', 'date_of_establishment', 'created_at', 'updated_at']
    search_fields = ['user', 'company_name', 'state']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name', 'created_at', 'updated_at']

class InventoryItemAdmin(admin.ModelAdmin):
    model = InventoryItem
    list_display = ['id', 'name', 'description', 'quantity', 'price', 'category', 'low_stock_threshold', 'created_at', 'updated_at']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'created_at', 'updated_at']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)