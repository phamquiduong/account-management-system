from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordField(serializers.CharField):
    default_error_messages = {
        "invalid": "Invalid password.",
    }

    def __init__(self, **kwargs):
        kwargs.setdefault("write_only", True)
        kwargs.setdefault("style", {"input_type": "password"})
        super().__init__(**kwargs)

    def run_validation(self, data):
        value = super().run_validation(data)
        validate_password(value)
        return value
