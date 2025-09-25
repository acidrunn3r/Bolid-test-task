from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Sensor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
