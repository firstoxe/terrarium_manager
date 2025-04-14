import os
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

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
    HABITAT_CHOICES = [
        ('TROPICAL', 'Тропическая'),
        ('DESERT', 'Пустынная'),
        ('AQUATIC', 'Полуводная'),
    ]
    CARE_LEVEL_CHOICES = [
        ('BEGINNER', 'Новичок'),
        ('INTERMEDIATE', 'Средний'),
        ('EXPERT', 'Эксперт'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец")
    name = models.CharField("Кличка", max_length=100)
    taxonomy = models.ForeignKey('Taxonomy', on_delete=models.PROTECT, verbose_name="Таксон")
    morph = models.ForeignKey('Morph', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Морфа")
    birth_date = models.DateField("Дата рождения/вылупления")
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    acquisition_date = models.DateField("Дата приобретения", auto_now_add=True)
    photo = models.ImageField("Фото", upload_to='animals/', blank=True)
    notes = models.TextField("Заметки", blank=True)
    habitat = models.CharField("Среда обитания", max_length=20, choices=HABITAT_CHOICES)
    care_level = models.CharField("Сложность ухода", max_length=20, choices=CARE_LEVEL_CHOICES)

    def generate_upload_path(self, filename):
        ext = filename.split('.')[-1]
        safe_filename = f"{slugify(self.name or 'animal')}-{uuid4().hex[:8]}.{ext}"
        return os.path.join('animals', safe_filename)

    def save(self, *args, **kwargs):
        if self.pk:
            # Получаем старый объект из базы
            old = Animal.objects.filter(pk=self.pk).first()
            if old and old.photo != self.photo and self.photo:
                # Только если фото новое — меняем имя
                self.photo.name = self.generate_upload_path(self.photo.name)
        elif self.photo:
            # Новый объект — сразу задаём имя
            self.photo.name = self.generate_upload_path(self.photo.name)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"
        ordering = ['-acquisition_date']

    def __str__(self):
        return f"{self.name} ({self.taxonomy.species})"

    def get_absolute_url(self):
        return reverse('animals:animal_detail', kwargs={'pk': self.pk})


class Taxonomy(models.Model):
    class_name = models.CharField("Класс", max_length=100, blank=True)
    order = models.CharField("Отряд", max_length=100, blank=True)
    family = models.CharField("Семейство", max_length=100, blank=True)
    genus = models.CharField("Род", max_length=100, blank=True)
    species = models.CharField("Вид", max_length=100, unique=True)
    subspecies = models.CharField("Подвид", max_length=100, blank=True)
    scientific_name = models.CharField("Научное название", max_length=200, unique=True)

    class Meta:
        verbose_name = "Таксон"
        verbose_name_plural = "Таксоны"

    def __str__(self):
        return f"{self.scientific_name} ({self.species})"


class Morph(models.Model):
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, verbose_name="Таксон")
    name = models.CharField("Название морфы", max_length=100)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Морфа"
        verbose_name_plural = "Морфы"
        unique_together = ('taxonomy', 'name')

    def __str__(self):
        return f"{self.name} ({self.taxonomy.species})"


class Action(models.Model):
    ACTION_TYPES = [
        ('FEEDING', 'Кормление'),
        ('CLEANING', 'Уборка'),
        ('TREATMENT', 'Лечение'),
        ('BREEDING', 'Размножение'),
        ('OBSERVATION', 'Наблюдение'),
        ('OTHER', 'Другое'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Животное")
    action_type = models.CharField("Тип действия", max_length=20, choices=ACTION_TYPES)
    date = models.DateTimeField("Дата и время", default=timezone.now)
    description = models.TextField("Описание")
    cost = models.DecimalField(verbose_name='Затраты', max_digits=10, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Автор")

    class Meta:
        verbose_name = "Действие"
        verbose_name_plural = "Действия"
        ordering = ['-date']

    def __str__(self):
        return f"{self.action_type} для {self.animal.name} ({self.date})"


class CareRequirement(models.Model):
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE, verbose_name="Таксон")
    temperature_min = models.FloatField("Минимальная температура (°C)")
    temperature_max = models.FloatField("Максимальная температура (°C)")
    humidity_min = models.FloatField("Минимальная влажность (%)")
    humidity_max = models.FloatField("Максимальная влажность (%)")
    diet = models.TextField("Рацион")
    lighting = models.TextField("Освещение", blank=True)
    substrate = models.TextField("Субстрат", blank=True)

    class Meta:
        verbose_name = "Требование по уходу"
        verbose_name_plural = "Требования по уходу"

    def __str__(self):
        return f"Уход для {self.taxonomy.species}"
