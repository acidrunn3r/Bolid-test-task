import json
import tempfile

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from sensors.models import Event, Sensor


class SensorModelTest(TestCase):
    def test_create_sensor(self):
        sensor = Sensor.objects.create(id=123, name="Temperature", type=1)
        self.assertEqual(sensor.id, 123)
        self.assertEqual(sensor.name, "Temperature")
        self.assertEqual(sensor.type, 1)

    def test_sensor_name_validator(self):
        with self.assertRaises(ValidationError):
            sensor = Sensor(id=1, name="Bad#Name", type=1)
            sensor.full_clean()

    def test_update_sensor(self):
        sensor = Sensor.objects.create(id=1, name="Test", type=2)
        sensor.name = "Updated"
        sensor.save()
        self.assertEqual(Sensor.objects.get(id=1).name, "Updated")

    def test_delete_sensor(self):
        sensor = Sensor.objects.create(id=2, name="ToDelete", type=3)
        sensor_id = sensor.id
        sensor.delete()
        self.assertFalse(Sensor.objects.filter(id=sensor_id).exists())


class EventModelTest(TestCase):
    def setUp(self):
        self.sensor = Sensor.objects.create(id=10, name="MainSensor", type=1)

    def test_create_event(self):
        event = Event.objects.create(
            sensor_id=self.sensor, name="Temperature", temperature=42.5, humidity=50.0
        )
        self.assertEqual(event.sensor_id, self.sensor)
        self.assertEqual(event.name, "Temperature")
        self.assertEqual(event.temperature, 42.5)
        self.assertEqual(event.humidity, 50.0)

    def test_event_without_sensor_fails(self):
        with self.assertRaises(ValidationError):
            event = Event(name="Pressure", temperature=101.3)
            event.full_clean()


class SensorAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sensor = Sensor.objects.create(id=100, name="API Sensor", type=1)

    def test_list_sensors(self):
        response = self.client.get(reverse("sensor-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_create_sensor(self):
        data = {"id": 101, "name": "NewSensor", "type": 2}
        response = self.client.post(reverse("sensor-list", kwargs={"version": "v1"}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sensor.objects.filter(id=101).count(), 1)

    def test_retrieve_sensor(self):
        response = self.client.get(
            reverse("sensor-detail", kwargs={"version": "v1", "pk": self.sensor.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], 100)

    def test_update_sensor(self):
        data = {"id": 100, "name": "RenamedSensor", "type": 1}
        response = self.client.put(
            reverse("sensor-detail", kwargs={"version": "v1", "pk": self.sensor.pk}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sensor.objects.get(pk=self.sensor.pk).name, "RenamedSensor")

    def test_delete_sensor(self):
        response = self.client.delete(
            reverse("sensor-detail", kwargs={"version": "v1", "pk": self.sensor.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Sensor.objects.filter(pk=self.sensor.pk).exists())


class EventAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sensor = Sensor.objects.create(id=200, name="Sensor200", type=1)
        self.event = Event.objects.create(
            sensor_id=self.sensor, name="Temperature", temperature=25.0, humidity=40.0
        )

    def test_list_events(self):
        response = self.client.get(reverse("event-list", kwargs={"version": "v1"}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.json()), 1)

    def test_create_event(self):
        data = {"sensor_id": self.sensor.id, "name": "Humidity", "humidity": 60.5}
        response = self.client.post(reverse("event-list", kwargs={"version": "v1"}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.filter(name="Humidity").count(), 1)

    def test_retrieve_event(self):
        response = self.client.get(
            reverse("event-detail", kwargs={"version": "v1", "pk": self.event.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Temperature")

    def test_update_event(self):
        data = {
            "sensor_id": self.sensor.id,
            "name": "Pressure",
            "temperature": 101.3,
            "humidity": 55.0,
        }
        response = self.client.put(
            reverse("event-detail", kwargs={"version": "v1", "pk": self.event.pk}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Pressure")
        self.assertEqual(self.event.temperature, 101.3)
        self.assertEqual(self.event.humidity, 55.0)

    def test_delete_event(self):
        response = self.client.delete(
            reverse("event-detail", kwargs={"version": "v1", "pk": self.event.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())


class UploadJSONTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.sensor = Sensor.objects.create(id=300, name="UploadSensor", type=1)

    def test_upload_events_from_json(self):
        events_data = [
            {
                "sensor_id": self.sensor.id,
                "name": "Temperature",
                "temperature": 22.5,
                "humidity": 50.0,
            },
            {"sensor_id": self.sensor.id, "name": "Humidity", "humidity": 55.0},
        ]
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp_file.write(json.dumps(events_data).encode("utf-8"))
        tmp_file.seek(0)

        with open(tmp_file.name, "rb") as f:
            response = self.client.post(
                reverse("event-upload-json", kwargs={"version": "v1"}),
                {"file": f},
                format="multipart",
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
