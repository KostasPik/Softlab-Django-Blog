from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, BaseUserManager
from django.db.models.fields import related
# Create your models here.
from posts.models import Post

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, email_verified=True, **extra_fields)



class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    is_premium = models.BooleanField(default=False) # if user is premium... by paying some type of subscription (not yet implemented).
    email_verified = models.BooleanField(default=False) # if user is verified.
    
    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username