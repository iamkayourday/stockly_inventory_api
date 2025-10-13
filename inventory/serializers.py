from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import (Category, CustomUser, InventoryChange, InventoryItem, Notification,
                     Profile, Supplier)


# 1. User Registration Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'middle_name','password', 'confirm_password',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'middle_name': {'required': True},
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data['middle_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# 2. Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'updated_at', 'created_at')


# 3. Only Admin users should see all fields
class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    phone_number = serializers.CharField(source='profile.phone_number', read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'middle_name', 'is_staff', 'is_active', 'date_joined', 'profile', 'phone_number')

# 4. Password Change Serializer
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, 
        validators=[validate_password]
    )
    confirm_new_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        # Check password match
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError(
                {"confirm_new_password": "New password fields didn't match."}
            )
        
        # Check old password validity
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct."}
            )

        return attrs

# 5. Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

# 6. Inventory Item Serializer
class InventoryItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    user = serializers.ReadOnlyField(source='user.username')
    is_low_stock = serializers.ReadOnlyField()
    total_value = serializers.ReadOnlyField()

    class Meta:
        model = InventoryItem
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'is_low_stock', 'total_value')

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        elif len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value
    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value
    def validate_low_stock_threshold(self, value):
        if value < 0:
            raise serializers.ValidationError("Low stock threshold cannot be negative.")
        return value
    def validate(self, attrs):
        if 'quantity' in attrs and 'low_stock_threshold' in attrs:
            if attrs['quantity'] < attrs['low_stock_threshold']:
                raise serializers.ValidationError("Quantity cannot be less than low stock threshold.")
        return attrs

# 7. Inventory Item Update Serializer
class InventoryItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = ['name','price', 'description', 'low_stock_threshold', 'category', 'supplier']  

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_low_stock_threshold(self, value):
        if value < 0:
            raise serializers.ValidationError("Low stock threshold cannot be negative.")
        return value
    

# 8. Inventory Change Serializer
class InventoryChangeSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')
    user_name = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = InventoryChange
        fields = '__all__'
        read_only_fields = ('id', 'change_date', 'previous_quantity', 'new_quantity', 'user')

    def validate_quantity_change(self, value):
        if value == 0:
            raise serializers.ValidationError("Quantity change cannot be zero.")
        return value

    def validate(self, attrs):
        request = self.context.get('request')
        item = attrs.get('item')
        change_type = attrs.get('change_type')
        quantity_change = attrs.get('quantity_change')
        
        # Validate change type logic
        if change_type in ['SALE', 'DAMAGE'] and quantity_change > 0:
            raise serializers.ValidationError(
                {"quantity_change": f"{change_type} must have negative quantity change."}
            )
        
        if change_type in ['RESTOCK', 'RETURN'] and quantity_change < 0:
            raise serializers.ValidationError(
                {"quantity_change": f"{change_type} must have positive quantity change."}
            )
        
        # Prevent negative stock
        if item and quantity_change < 0:
            current_stock = item.quantity
            if current_stock + quantity_change < 0:
                raise serializers.ValidationError(
                    {"quantity_change": f"Cannot reduce stock below zero. Current: {current_stock}, Attempted: {quantity_change}"}
                )
        
        return attrs

# 9. Supplier Serializer 
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        elif len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']