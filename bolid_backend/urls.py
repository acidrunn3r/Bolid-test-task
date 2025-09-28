from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from sensors.views import EventViewSet, SensorViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Bolid Backend API",
        default_version="v1",
        description="Документация API для проекта Bolid Backend",
        contact=openapi.Contact(email="lipov.sa@mail.ru"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)

router = DefaultRouter()
router.register("sensors", SensorViewSet)
router.register("events", EventViewSet)


urlpatterns = [
    path("", RedirectView.as_view(url="/api/<version>/", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/<version>/", include(router.urls)),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
