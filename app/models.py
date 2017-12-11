from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.
class UserProfileManager(BaseUserManager):
    """helps django work with our custom user manager"""

    def create_user(self,email,name,password=None):
        """creates a new user profile object"""
        if not email:   #since email is a required address
            raise ValueError('Users must have an email error')
        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        """creates a new superuser with given details"""
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Represents a user profile inside our system"""
    # add fields to the model
    #fields are pieces of data you collect from model and stores in database

    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #set object manager(used to manage class above)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    #some helper functions
    def get_full_name(self):
        """used to get a user full name"""

        return self.name

    def get_short_name(self):
        """Used to get a user short name"""

        return self.name

    def __str__(self):
        """django uses this to convert the object to a string"""

        return self.email