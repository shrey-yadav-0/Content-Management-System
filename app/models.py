from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        role = Role.objects.get(name='Author')
        extra_fields["role"] = role
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        role = Role.objects.get(name='Admin')
        extra_fields["role"] = role
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, validators=[
        RegexValidator(r'^\d{10}$', 'Phone number must be exactly 10 digits')
    ])
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=6, validators=[
        RegexValidator(r'^\d{6}$', 'Pincode must be exactly 6 digits')
    ])
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "pincode"]

    def __str__(self):
        return self.email


class Content(models.Model):
    title = models.CharField(max_length=30, blank=False, null=False)
    body = models.CharField(max_length=300, blank=False, null=False)
    summary = models.CharField(max_length=60, blank=False, null=False)
    document = models.FileField(upload_to="pdfs/", blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ContentCategory(models.Model):
    content = models.ForeignKey(Content, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
