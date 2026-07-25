from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


@extend_schema(exclude=True)
class HiddenSpectacularAPIView(SpectacularAPIView):
    pass


api_router = [
    path("schema/", HiddenSpectacularAPIView.as_view(), name="api_schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api_schema"), name="swagger-ui"),
    path("re-doc/", SpectacularRedocView.as_view(url_name="api_schema"), name="redoc"),
]


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_router)),
    path("auth/", include("authentication.urls")),
    path("account/", include("account.urls")),
]
