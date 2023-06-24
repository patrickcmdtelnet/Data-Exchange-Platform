import factory
from factory.django import DjangoModelFactory
from django.utils.translation import gettext_lazy as _
from core.models import (
    PrivateSector,
    PublicSector,
    Academia,
    Ministry,
    Organization,
    User,
)
from faker import Faker

fake = Faker()


class PrivateSectorFactory(DjangoModelFactory):
    class Meta:
        model = PrivateSector

    name = factory.Faker("company")


class PublicSectorFactory(DjangoModelFactory):
    class Meta:
        model = PublicSector

    name = factory.Faker("company")


class AcademiaFactory(DjangoModelFactory):
    class Meta:
        model = Academia

    name = factory.Faker("university")


class MinistryFactory(DjangoModelFactory):
    class Meta:
        model = Ministry

    name = factory.Faker("company")


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker("company")
    acronym = factory.Faker("word")
    type = Organization.Type.PRIVATE_SECTOR


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    organization = factory.SubFactory(OrganizationFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("ascii_safe_email")
    password = factory.Faker("password")
    phone_number = fake.unique.numerify("07#######")
    username = factory.Faker("user_name")
    permission_level = User.PermissionLevel.USER_ROLE
