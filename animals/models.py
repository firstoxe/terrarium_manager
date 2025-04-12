from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Species(models.Model):
    name = models.CharField("Название вида", max_length=100, unique=True)
    scientific_name = models.CharField("Научное название", max_length=100)

    class Meta:
        verbose_name = "Вид"
        verbose_name_plural = "Виды"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('animals:species_select')


class Animal(models.Model):
    SEX_CHOICES = [
        ('M', 'Самец'),
        ('F', 'Самка'),
        ('U', 'Неизвестно')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    name = models.CharField("Кличка", max_length=100)
    species = models.ForeignKey(Species, on_delete=models.PROTECT, verbose_name="Вид")
    birth_date = models.DateField("Дата рождения/вылупления")
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    acquisition_date = models.DateField("Дата приобретения", auto_now_add=True)
    photo = models.ImageField("Фото", upload_to='animals/', blank=True)
    notes = models.TextField("Заметки", blank=True)

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"
        ordering = ['-acquisition_date']

    def __str__(self):
        return f"{self.name} ({self.species})"

    def get_absolute_url(self):
        return reverse('animals:detail', kwargs={'pk': self.pk})
