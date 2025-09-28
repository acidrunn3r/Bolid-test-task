from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Sensor(models.Model):
    """
    Модель сенсора (датчика).

    Поля:
    - id: первичный ключ, целое положительное число.
    - name: название сенсора, только русские/латинские буквы, цифры, '-' и '/'.
    - type: тип сенсора, целое число от 1 до 3.
    """

    id = models.IntegerField(
        primary_key=True, help_text="ID сенсора, целое положительное число"
    )
    name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[а-яА-Яa-zA-Z0-9\-/]+$",
                message=(
                    "Имя датчика может содержать только русские и латинские буквы, "
                    "цифры, тире и слеш"
                ),
            )
        ],
        help_text="Название сенсора, только буквы, цифры, '-' и '/'",
    )
    type = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="Тип сенсора: целое число от 1 до 3",
    )

    def __str__(self):
        return f"Датчик {self.id}: {self.name}."

    class Meta:
        db_table = "Датчики"
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"


class Event(models.Model):
    """
    Модель события.

    Поля:
    - id: первичный ключ, автоинкремент.
    - sensor_id: внешний ключ на Sensor.
    - name: название события, только русские/латинские буквы, цифры.
    - '_', N/A, может быть пустым.
    - temperature: температура, float, от -273.15 до 5499.0, может быть пустым.
    - humidity: влажность, float, от 0 до 100, может быть пустой.
    - created_at: дата и время создания события, автоматически.
    """

    id = models.AutoField(primary_key=True, help_text="ID события, автоинкремент")
    sensor_id = models.ForeignKey(
        "Sensor",
        related_name="events",
        on_delete=models.CASCADE,
        help_text="Сенсор, которому принадлежит событие",
    )
    name = models.CharField(
        max_length=50,
        blank=True,  # разрешает оставлять пустым в формах и сериализаторах
        null=True,  # разрешает хранить NULL в базе данных
        validators=[
            RegexValidator(
                regex=r"^([а-яА-Яa-zA-Z0-9_]+|N/A)?$",
                message=(
                    "Название события может содержать только русские и латинские буквы, "
                    "цифры, '_', и N/A."
                ),
            )
        ],
        help_text="Название события",
    )
    temperature = models.FloatField(
        validators=[MinValueValidator(-273.15), MaxValueValidator(5499.0)],
        null=True,
        blank=True,
        help_text="Температура события (°C), от -273.15 до 5499.0, может быть пустой",
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        null=True,
        blank=True,
        help_text="Влажность события (%), от 0 до 100, может быть пустой",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата и время создания события"
    )

    def __str__(self):
        return f"Событие {self.id}: {self.name or 'N/A'} от датчика {self.sensor_id.id}."

    class Meta:
        db_table = "События"
        verbose_name = "Событие"
        verbose_name_plural = "События"
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["sensor_id"]),
            models.Index(fields=["sensor_id", "created_at"]),
            models.Index(fields=["temperature"]),
            models.Index(fields=["humidity"]),
        ]
