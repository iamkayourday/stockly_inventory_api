import shortuuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Custom user model
class CustomUser(AbstractUser):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        default=shortuuid.uuid,
        editable=False,
        unique=True,
        db_index=True  # For faster queries (nice for APIs)
    )

    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)  
    middle_name = models.CharField(max_length=30, blank=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.username

    def get_full_name(self):
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{middle} {self.last_name}".strip()


# Profile model linked to CustomUser
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    company_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    tax_id = models.CharField(max_length=100, blank=True)
    business_type = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    date_of_establishment = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.email}'s Profile"


# Category model
class Category(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
# Inventory Item Model
class InventoryItem(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
    # Property to check if the item is low in stock
    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
    
    # Property to calculate total value of the inventory item
    @property
    def total_value(self):
        return self.quantity * self.price