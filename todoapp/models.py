import datetime
import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
from django.utils import timezone
import datetime

DISCOUNT_CODE_TYPES_CHOICES = [
    ("percent", "Percentage-based"),
    ("value", "Value-based"),
]


# Create your models here
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class EtatModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "etats"

    def __str__(self):
        return self.value


class CategoryModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.value


class TaskModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    etat = models.ForeignKey(EtatModel, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, null=True, related_name="tasks"
    )
    deadline = models.DateField(default=datetime.date.today())
    is_urgent = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tasks"
        ordering = ["-createdAt"]

    def __str__(self):
        return self.title
