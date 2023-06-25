from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from core.common import DateTimeStampMixin
from core.managers import UserManager
from utils.constants import (
    ACADEMIA,
    CONTACT_ADMIN,
    PRIVATE_SECTOR,
    PUBLIC_SECTOR,
    SUPER_ADMIN,
    USER_ROLE,
)


class PrivateSector(DateTimeStampMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PublicSector(DateTimeStampMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Academia(DateTimeStampMixin):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ministry(DateTimeStampMixin):
    class Meta:
        verbose_name_plural = "ministries"

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Organization(DateTimeStampMixin):
    class Type(models.TextChoices):
        PRIVATE_SECTOR = PRIVATE_SECTOR, _("Private Sector")
        PUBLIC_SECTOR = PUBLIC_SECTOR, _("Public Sector")
        ACADEMIA = ACADEMIA, _("Academia")

    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=30,
        choices=Type.choices,
        default=Type.PRIVATE_SECTOR,
    )
    acronym = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    class PermissionLevel(models.TextChoices):
        SUPER_ADMIN = SUPER_ADMIN, _("Super Admin")
        CONTACT_ADMIN = SUPER_ADMIN, _("Contact Admin")
        USER_ROLE = "USER", _("User")

    organization = models.ForeignKey(
        Organization,
        related_name="organizations",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True, db_index=True)
    password = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    permission_level = models.CharField(
        max_length=30,
        choices=PermissionLevel.choices,
        default=PermissionLevel.USER_ROLE,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "organization_id"]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
