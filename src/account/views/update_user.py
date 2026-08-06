from http import HTTPMethod

from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from account.serializers.update_user import UpdateUserSerializer


@extend_schema(tags=["Account"])
class UpdateUserView(generics.UpdateAPIView):
    http_method_names = (HTTPMethod.PATCH.lower(),)
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
