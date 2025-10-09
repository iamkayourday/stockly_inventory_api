import shortuuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# CUSTOM USER MODEL
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
    middle_name = models.CharField(max_length=30, blank=True) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.username

    def get_full_name(self):
        middle = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.first_name}{middle} {self.last_name}".strip()


# PROFILE MODEL LINKED CUSTOMUSER MODEL
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=100, blank=True)
    facebook_username = models.CharField(max_length=100, blank=True)
    instagram_username = models.CharField(max_length=100, blank=True)
    twitter_username = models.CharField(max_length=100, blank=True)
    tiktok_username = models.CharField(max_length=100, blank=True)
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


# STRETCH GOAL
# CATEGORY MODEL
class Category(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False, unique=True)
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

# STRETCH GOAL
# SUPPLIER MODEL
class Supplier(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False, unique=True)
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='suppliers', null=True)
    contact_person = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
   
# INVENTORY ITEM MODEL LINKED TO CATEGORY AND SUPPLIER MODEL
class InventoryItem(models.Model):
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False, unique=True)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_items', null=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# STRETCH GOALS
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, related_name='supplied_items')


    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} ({self.quantity})"
    
    # Property to check if the item is low in stock
    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
    
    @property
    def total_products(self):
        return self.inventory_items.count()

    @property
    def total_value(self):
        if self.price is not None and self.quantity is not None:
            return self.quantity * self.price
        return 0 
    

#  Inventory Change Model
class InventoryChange(models.Model):
    CHANGE_TYPE = [
        ('RESTOCK', 'Restock'),
        ('SALE', 'Sale'),
        ('RETURN', 'Return'),
        ('DAMAGE', 'Damage'),
    ]
    id = models.CharField(primary_key=True, default=shortuuid.uuid, max_length=22, editable=False, unique=True)
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='changes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_changes', null=True)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE)
    quantity_change = models.IntegerField()  
    previous_quantity = models.PositiveIntegerField(null=True, blank=True, default=0)  
    new_quantity = models.PositiveIntegerField(null=True, blank=True, default=0)
    reason = models.TextField(blank=True)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change_type} - {self.item.name} ({self.quantity_change})"
    
    def save(self, *args, **kwargs):
    # Prevent circular quantity updates
        if self.item:
            if not (self.reason == 'Initial stock entry' and self.change_type == 'RESTOCK'):
                self.previous_quantity = self.item.quantity

                if self.change_type in ['SALE', 'DAMAGE']:
                    self.new_quantity = self.previous_quantity - self.quantity_change
                else:  # RESTOCK or RETURN
                    self.new_quantity = self.previous_quantity + self.quantity_change

                # Update the inventory item
                self.item.quantity = self.new_quantity
                self.item.save()
            else:
                # For initial stock, just log the current state
                self.previous_quantity = 0
                self.new_quantity = self.item.quantity

        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-change_date']
        
