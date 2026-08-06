from rest_framework import serializers

from common.fields.password import PasswordField
from common.utils.black_list import blacklist_all_tokens


class ChangePasswordSerializer(serializers.Serializer):
    old_password = PasswordField()
    new_password = PasswordField()

    message = serializers.CharField(read_only=True, default="Update password successfully")

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])

        blacklist_all_tokens(instance)

        return instance
