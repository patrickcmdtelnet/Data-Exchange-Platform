"""
Tests for models.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models
from core.tests import factories
from utils.constants import SUPER_ADMIN


def create_superuser(email="user@example.com", password="testpass123"):
    """Create and return new user."""
    user = factories.UserFactory(email=email, password=email)
    user.is_verified = True
    user.is_staff = True
    user.is_superuser = True
    user.permission_level = SUPER_ADMIN
    user.save()
    return user


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            is_verified=True,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_verified)
        self.assertEqual(user.permission_level, SUPER_ADMIN)

    def test_create_private_sector(self):
        """Test creating a private sector is successful."""
        sector = factories.PrivateSectorFactory(name="Test Private Sector")

        self.assertEqual(str(sector), sector.name)

    def test_create_public_sector(self):
        """Test creating a public sector is successful."""
        sector = factories.PublicSectorFactory(name="Test Public Sector")

        self.assertEqual(str(sector), sector.name)

    def test_create_academia(self):
        """Test creating a academia is successful."""
        academia = factories.AcademiaFactory(name="Test Academia")

        self.assertEqual(str(academia), academia.name)

    def test_create_ministry(self):
        """Test creating a ministry is successful."""
        ministry = factories.MinistryFactory(name="Test Ministry")

        self.assertEqual(str(ministry), ministry.name)

    def test_create_organization(self):
        """Test creating an organization is successful."""
        org = factories.OrganizationFactory(name="Test Organization")

        self.assertEqual(str(org), org.name)
