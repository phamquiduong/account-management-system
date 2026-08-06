from django.urls import include, path
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


@extend_schema(exclude=True)
class HiddenSpectacularAPIView(SpectacularAPIView):
    pass


urlpatterns = [
    path("schema/", HiddenSpectacularAPIView.as_view(), name="api_schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="api_schema"), name="swagger-ui"),
    path("re-doc/", SpectacularRedocView.as_view(url_name="api_schema"), name="re-doc"),
    path("auth/", include("authentication.urls_api")),
    path("account/", include("account.urls_api")),
]
