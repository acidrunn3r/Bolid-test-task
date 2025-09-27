from django_filters.rest_framework import FilterSet, NumberFilter
from rest_framework.exceptions import ValidationError
from .models import Event

class EventFilter(FilterSet):
    temperature_min = NumberFilter(field_name="temperature", lookup_expr='gte', label="Minimal Temperature")
    temperature_max = NumberFilter(field_name="temperature", lookup_expr='lte', label="Maximal Temperature")
    humidity_min = NumberFilter(field_name="humidity", lookup_expr='gte', label="Minimal Humidity")
    humidity_max = NumberFilter(field_name="humidity", lookup_expr='lte', label="Maximal Humidity")

    class Meta:
        model = Event
        fields = ['sensor_id', 'temperature', 'humidity']

    def filter_queryset(self, queryset):
        temp_min = self.data.get('temperature_min')
        temp_max = self.data.get('temperature_max')
        if temp_min and temp_max and float(temp_max) < float(temp_min):
            raise ValidationError("temperature_max не может быть меньше temperature_min")
        humi_min = self.data.get('humidity_min')
        humi_max = self.data.get('humidity_max')
        if humi_min and humi_max and float(humi_max) < float(humi_min):
            raise ValidationError("humidity_max не может быть меньше humidity_min")
        return super().filter_queryset(queryset)