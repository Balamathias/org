from abc import abstractmethod
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.models import PermissionsMixin

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    @abstractmethod
    def create_user(self, email, firstName, lastName, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not firstName:
            raise ValueError('Users must have a first name')
        if not lastName:
            raise ValueError('Users must have a last name')
        if not phone:
            raise ValueError('Users must have a phone number')

        user = self.model(
            email=self.normalize_email(email),
            firstName=firstName,
            lastName=lastName,
            phone=phone,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, firstName, lastName, phone, password=None):
        return self.create_user(email, firstName, lastName, phone, password, is_superuser=True, is_staff=True)


class Organization(models.Model):
    orgId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# class User(AbstractUser):
#     pass

class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    userId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    username = models.CharField(max_length=40, blank=True, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['firstName', 'lastName', 'phone']

    def get_full_name(self):
        return self.firstName + ' ' + self.lastName
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
