import json
import logging
from pathlib import Path

from django.core.management.base import BaseCommand

from sensors.models import Event, Sensor

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Импорт событий из JSON-файла"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Путь к JSON-файлу с событиями")

    def handle(self, *args, **options):
        json_path = Path(options["json_file"])
        if not json_path.exists():
            self.stderr.write(f"Файл {json_path} не найден.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(f"Ошибка при чтении JSON: {e}")
                return

        for item in data:
            sensor_id = item.get("sensor_id")
            name = item.get("name") or "N/A"
            temperature = item.get("temperature")
            humidity = item.get("humidity")

            if "status" in item:
                logger.warning(
                    f"Поле 'status' у события с sensor_id={sensor_id} проигнорировано"
                )

            # Проверка наличия датчика
            sensor, created = Sensor.objects.get_or_create(
                id=sensor_id, defaults={"name": "N/A", "type": 0}
            )
            if created:
                logger.warning(
                    f"Датчик с sensor_id={sensor_id} ранее не был в базе данных. "
                    f"Присваивается type = 0"
                )
            event = Event(
                sensor_id=sensor, name=name, temperature=temperature, humidity=humidity
            )
            try:
                event.full_clean()  #
                event.save()
                self.stdout.write(f"Событие {event.id} добавлено (sensor_id={sensor_id})")
            except Exception as e:
                self.stderr.write(
                    f"Ошибка при добавлении события для sensor_id={sensor_id}: {e}"
                )
