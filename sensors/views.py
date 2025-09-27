from rest_framework import viewsets, filters

from .filters import EventFilter
from .models import Sensor, Event
from .serializers import SensorSerializer, EventSerializer
from django_filters.rest_framework import DjangoFilterBackend

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'id']
    ordering = ['id']

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = EventFilter
    ordering_fields = ['created_at']
    ordering = ['-created_at']

