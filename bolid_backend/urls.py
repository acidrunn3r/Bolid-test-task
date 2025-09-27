from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from sensors.views import EventViewSet, SensorViewSet

router = DefaultRouter()
router.register("sensors", SensorViewSet)
router.register("events", EventViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/<version>/", include(router.urls)),
]
