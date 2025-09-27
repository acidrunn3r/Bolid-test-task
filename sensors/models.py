from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models


class Sensor(models.Model):
    id = models.IntegerField(primary_key=True)
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
    )
    type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])

    def __str__(self):
        return f"Датчик {self.id}: {self.name}."

    class Meta:
        db_table = "Датчики"
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    sensor_id = models.ForeignKey(Sensor, related_name="events", on_delete=models.CASCADE)
    name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^([а-яА-Яa-zA-Z0-9_]+|N/A)?$",
                message=(
                    "Название события может содержать только русские и латинские буквы,"
                    " цифры, _,  и N/A."
                ),
            )
        ],
    )
    temperature = models.FloatField(
        validators=[MinValueValidator(-273.15), MaxValueValidator(5499.0)],
        null=True,
        blank=True,
    )
    humidity = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Событие {self.id}: {self.name} от датчика {self.sensor_id.id}."

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
