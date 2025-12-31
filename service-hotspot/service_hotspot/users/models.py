from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model with primary fields: mobile number and email.
    """
    mobile_number = models.CharField(_("Mobile Number"), max_length=15, unique=True, blank=False)
    email = models.EmailField(_("Email Address"), unique=True, blank=False)

    # Remove first_name and last_name from the default user model
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

class UserProfile(models.Model):
    """
    User profile model for storing additional user information.
    Linked to the main User model through a One-to-One relationship.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullname = models.CharField(max_length=50, null=True)
    address = models.JSONField(default=dict, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    accepted_method = models.CharField(max_length=100, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
