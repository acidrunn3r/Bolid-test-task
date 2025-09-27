from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .filters import EventFilter
from .models import Event, Sensor
from .serializers import EventSerializer, SensorSerializer


class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "id"]
    ordering = ["id"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
