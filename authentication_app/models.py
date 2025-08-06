from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,username, email, phone_number, password = None, role='USER'):
        if not email:
            raise ValueError("Email field is required")
        
        user = self.model(
            username = username,
            email=self.normalize_email(email),
            phone_number=phone_number,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username, email, phone_number, password = None):
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            role='ADMIN'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
class User(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('USER', 'User'),
        ('OFFICER', 'Officer'),
        ('ADMIN', 'Admin')
    ]
    
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number= models.CharField(max_length=255)
    role=models.CharField(max_length=100, choices=ROLES, default='USER')
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']
    
    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def is_admin(self):
        return self.is_staff