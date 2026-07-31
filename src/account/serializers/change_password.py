from rest_framework import serializers

from common.fields.password import PasswordField


class ChangePasswordSerializer(serializers.Serializer):
    old_password = PasswordField()
    new_password = PasswordField()

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
