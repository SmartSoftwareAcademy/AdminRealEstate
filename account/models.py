from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
# from tenants.models import Tenant

mobile_num_regex = RegexValidator(
        regex=r"^(?:\+254|0)[17]\d{8}$", message="Entered mobile number isn't in a right format!"
    )

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"),(2, "Agent"),(3,"Tenant"),(4,"Staff"))
    GENDER = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    username = models.CharField(max_length=150, unique=True,blank=True,null=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=1)
    gender = models.CharField(max_length=10, choices=GENDER)
    profile_pic = models.ImageField(upload_to='profiles',blank=True,null=True)
    other_name = models.CharField(max_length=200, blank=True)
    address = models.TextField()
    fcm_token = models.TextField(default="")  # For firebase notifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = slugify(self.email.split('@')[0])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.last_name + ", " + self.first_name

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # if instance.user_type == 1:
    #     instance.owners.save()
    # if instance.user_type == 2:
    #     instance.agents.save()
    # if instance.user_type == 2:
    #     instance.tenants.save()
    pass