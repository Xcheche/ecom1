from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from accounts.manager import CustomUserManager
# Create your models here.


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    about = models.TextField(blank=True, null=True)  # Optional field for user bio or description
    user_name = models.CharField(max_length=30, unique=True)
    
    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # This is used to check if the user can access the admin site
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    USERNAME_FIELD = 'email' # This is the field that will be used to log in
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name'] # Can add phone number i desired to make it requierd field
    
    
    objects = CustomUserManager() # Custom user manager
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None): # Check if the user has a specific permission
        return self.is_admin
    
    def has_module_perms(self, app_label): # Check if the user has permissions to view the app
        return True