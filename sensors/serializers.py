from rest_framework import serializers

from sensors.models import Event, Sensor


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = (
            "id",
            "name",
            "type",
        )


class EventSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    sensor_id = serializers.PrimaryKeyRelatedField(queryset=Sensor.objects.all())

    class Meta:
        model = Event
        fields = (
            "sensor_id",
            "name",
            "temperature",
            "humidity",
            "id",
        )
