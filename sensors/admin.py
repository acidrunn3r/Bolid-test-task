from django.contrib import admin
from .models import Sensor, Event

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    search_fields = ('name', 'id')
    ordering = ('id',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sensor_id', 'temperature', 'humidity', 'created_at')
    list_filter = ('sensor_id', 'created_at', 'temperature', 'humidity')
    search_fields = ('name', 'sensor_id__id')
    ordering = ('-created_at',)
