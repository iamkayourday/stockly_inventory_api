from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Category, CustomUser, InventoryChange, InventoryItem,
                     Profile, Supplier)


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['id', 'email', 'username', 'first_name', 'middle_name', 'last_name','is_staff', 'is_active', 'last_login', 'date_joined',
    ]

    fieldsets = (
        (None, {'fields': ('email', 'password', 'username', 'first_name', 'middle_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username',  'first_name', 'middle_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ['user','company_name', 'address', 'website', 'city', 'state', 'country', 'postal_code',  'tax_id', 'business_type','about','logo', 'date_of_establishment', 'created_at', 'updated_at']
    search_fields = ['user', 'company_name', 'state']

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name', 'created_at', 'updated_at']

class InventoryItemAdmin(admin.ModelAdmin):
    model = InventoryItem
    list_display = ['id', 'name', 'supplier', 'barcode', 'description', 'quantity', 'price', 'category', 'low_stock_threshold', 'created_at', 'updated_at']
    # readonly_fields = ('quantity', 'created_at', 'updated_at', 'total_value', 'is_low_stock')
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'created_at', 'updated_at']

class InventoryChangeAdmin(admin.ModelAdmin):
    model = InventoryChange
    list_display = ['id', 'item', 'change_type', 'quantity_change', 'previous_quantity', 'new_quantity', 'user', 'change_date']
    list_filter = ['change_type', 'change_date']
    search_fields = ['item__name', 'user__username', 'reason']
    readonly_fields = ['previous_quantity', 'new_quantity', 'change_date'] 

    def save_model(self, request, obj, form, change):
        """Ensure user is set and save method is called properly"""
        if not obj.pk:  # Only for new objects
            obj.user = request.user
        # This will trigger the custom save() method in the model
        super().save_model(request, obj, form, change)

class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    list_display = ['id', 'name', 'contact_person', 'email', 'phone_number', 'city', 'state', 'country', 'created_at', 'updated_at']
    search_fields = ['name', 'contact_person', 'email', 'phone_number']
    list_filter = ['city', 'state', 'country', 'created_at']
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(InventoryChange, InventoryChangeAdmin)
admin.site.register(Supplier, SupplierAdmin)