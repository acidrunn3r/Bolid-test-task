import json
import logging
from pathlib import Path

from sensors.models import Event, Sensor

logger = logging.getLogger(__name__)


def import_events_from_json(json_file: str):
    json_path = Path(json_file)
    if not json_path.exists():
        raise FileNotFoundError(f"Файл {json_path} не найден.")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    imported_events = []
    failed_events = []

    model_fields = {field.name for field in Event._meta.get_fields()}

    for item in data:
        sensor_id = item.get("sensor_id")
        extra_fields = set(item.keys()) - model_fields
        for field in extra_fields:
            logger.warning(
                f"Поле '{field}' у события с sensor_id={sensor_id} проигнорировано"
            )

        event_data = {
            k: v
            for k, v in item.items()
            if k in model_fields and k not in ["id", "sensor_id"]
        }

        if sensor_id <= 0:
            failed_events.append(
                {"sensor_id": sensor_id, "error": "sensor_id должен быть положительным"}
            )
            continue

        sensor, created = Sensor.objects.get_or_create(
            id=sensor_id, defaults={"name": "N/A", "type": 0}
        )
        if created:
            logger.warning(
                f"Датчик с sensor_id={sensor_id} ранее не был в базе данных. "
                f"Присваивается type = 0"
            )

        event = Event(sensor_id=sensor, **event_data)

        try:
            event.full_clean()
            event.save()
            imported_events.append(event.id)
        except Exception as e:
            logger.exception(f"Ошибка при добавлении события для sensor_id={sensor_id}")
            failed_events.append({"sensor_id": sensor_id, "error": str(e)})

    return {"imported": imported_events, "failed": failed_events}
