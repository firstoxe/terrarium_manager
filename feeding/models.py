from django.db import models
from animals.models import Animal


class Feeding(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date = models.DateTimeField("Дата кормления", auto_now_add=True)
    food_type = models.CharField("Тип корма", max_length=100)
    amount = models.PositiveIntegerField("Количество")

    def __str__(self):
        return f"{self.animal} - {self.food_type}"
