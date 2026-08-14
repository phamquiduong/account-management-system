from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import TimestampModel


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **extra_fields) -> "User":
        user = self.model(email=email, **extra_fields)
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_user(self, email: str, password: str, **extra_fields) -> "User":
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(TimestampModel, AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)

    first_name = None
    last_name = None
    name = models.CharField(_("name"), blank=True, null=True, max_length=255)

    is_verified_email = models.BooleanField(_("is verified email"), default=False)

    objects = UserManager()  # type:ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self._update_email_verified_status()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"User: {self.email}"

    class Meta:
        db_table = "users"

    def _update_email_verified_status(self) -> None:
        if self.pk:
            old_email = type(self).objects.only("email").get(pk=self.pk).email
            if old_email != self.email:
                self.is_verified_email = False
