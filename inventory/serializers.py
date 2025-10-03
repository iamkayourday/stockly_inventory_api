from rest_framework import serializers
from .models import CustomUser, Profile, Category
from django.contrib.auth.password_validation import validate_password

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
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'middle_name', 'phone_number', 'is_staff', 'is_active', 'date_joined', 'profile')

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