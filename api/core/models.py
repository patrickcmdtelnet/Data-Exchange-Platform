from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from core.managers import UserManager
from core.common import DateTimeStampMixin
from utils.constants import (
    SUPER_ADMIN,
    CONTACT_ADMIN,
    USER_ROLE,
    PRIVATE_SECTOR,
    PUBLIC_SECTOR,
    ACADEMIA,
)


class PrivateSector(DateTimeStampMixin):
    ps_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PublicSector(DateTimeStampMixin):
    ps_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Academia(DateTimeStampMixin):
    ac_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ministry(DateTimeStampMixin):
    class Meta:
        verbose_name_plural = "ministries"

    min_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Organization(DateTimeStampMixin):
    class Type(models.TextChoices):
        PRIVATE_SECTOR = PRIVATE_SECTOR, _("Private Sector")
        PUBLIC_SECTOR = PUBLIC_SECTOR, _("Public Sector")
        ACADEMIA = ACADEMIA, _("Academia")

    organization_id = models.BigAutoField(primary_key=True)
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

    user_id = models.BigAutoField(primary_key=True)
    organization = models.ForeignKey(
        Organization, related_name="organizations", on_delete=models.CASCADE, null=True, blank=True
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
