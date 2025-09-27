
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sensors.views import SensorViewSet, EventViewSet

router = DefaultRouter()
router.register('sensors', SensorViewSet)
router.register('events', EventViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/<version>/', include(router.urls))
]
