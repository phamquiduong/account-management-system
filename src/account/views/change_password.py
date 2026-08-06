from http import HTTPMethod

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.serializers.change_password import ChangePasswordSerializer
from common.utils.black_list import blacklist_all_tokens


@extend_schema(tags=["Account"])
class ChangePasswordView(generics.UpdateAPIView):
    http_method_names = [HTTPMethod.PATCH.lower()]
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        blacklist_all_tokens(request.user)
        return Response({"message": "Update password successfully"})
