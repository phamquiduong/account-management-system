from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("main.urls_api")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=f"{settings.STATIC_URL}images/favicon/favicon.ico", permanent=True),
    ),
]
