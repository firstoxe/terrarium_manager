import os
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Collection(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание', blank=True)
    is_global = models.BooleanField('Общая библиотека', default=False)
    share_token = models.CharField(
        'Публичный токен',
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
    )
    is_public = models.BooleanField('Публичная ссылка', default=False)

    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'

    def __str__(self):
        return self.name

    def ensure_share_token(self, *, rotate=False):
        import secrets
        if rotate or not self.share_token:
            self.share_token = secrets.token_urlsafe(24)
            self.save(update_fields=['share_token'])
        return self.share_token


class CollectionMember(models.Model):
    ROLE_CHOICES = [('viewer', 'Просмотр'), ('editor', 'Редактор')]
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')

    class Meta:
        unique_together = ('collection', 'user')


class Taxonomy(models.Model):
    class_name = models.CharField("Класс", max_length=100, blank=True)
    order = models.CharField("Отряд", max_length=100, blank=True)
    family = models.CharField("Семейство", max_length=100, blank=True)
    genus = models.CharField("Род", max_length=100, blank=True)
    species = models.CharField("Вид", max_length=100, unique=True)
    subspecies = models.CharField("Подвид", max_length=100, blank=True)
    scientific_name = models.CharField("Научное название", max_length=200, unique=True)
    common_name = models.CharField("Народное название", max_length=200, blank=True)
    library_id = models.CharField(
        "ID в справочнике",
        max_length=100,
        blank=True,
        null=True,
        unique=True,
    )
    is_global = models.BooleanField('Глобальный справочник', default=True)

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
    collection = models.ForeignKey(
        Collection, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='animals', verbose_name='Коллекция',
    )
    name = models.CharField("Кличка", max_length=100)
    taxonomy = models.ForeignKey('Taxonomy', on_delete=models.PROTECT, verbose_name="Таксон")
    morph = models.ForeignKey('Morph', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Морфа")
    parent_m = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='offspring_m', verbose_name='Отец',
    )
    parent_f = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='offspring_f', verbose_name='Мать',
    )
    birth_date = models.DateField("Дата рождения/вылупления")
    sex = models.CharField("Пол", max_length=1, choices=SEX_CHOICES)
    acquisition_date = models.DateField("Дата приобретения", default=timezone.localdate)
    photo = models.ImageField("Фото", upload_to='animals/', blank=True)
    notes = models.TextField("Заметки", blank=True)
    habitat = models.CharField("Среда обитания", max_length=20, choices=HABITAT_CHOICES)
    care_level = models.CharField("Сложность ухода", max_length=20, choices=CARE_LEVEL_CHOICES)

    def generate_upload_path(self, filename):
        ext = filename.split('.')[-1]
        safe_filename = f"{slugify(self.name or 'animal')}-{uuid4().hex[:8]}.{ext}"
        return os.path.join('animals', safe_filename)

    def save(self, *args, **kwargs):
        old_photo = None
        if self.pk:
            old = Animal.objects.filter(pk=self.pk).first()
            if old and old.photo and old.photo != self.photo:
                old_photo = old.photo
            if old and old.photo != self.photo and self.photo:
                self.photo.name = self.generate_upload_path(self.photo.name)
        elif self.photo:
            self.photo.name = self.generate_upload_path(self.photo.name)

        super().save(*args, **kwargs)

        if old_photo and (not self.photo or old_photo.name != self.photo.name):
            old_photo.delete(save=False)

    class Meta:
        verbose_name = "Животное"
        verbose_name_plural = "Животные"
        ordering = ['-acquisition_date']

    def __str__(self):
        return f"{self.name} ({self.taxonomy.species})"

    def get_absolute_url(self):
        return reverse('animals:animal_detail', kwargs={'pk': self.pk})


def animal_gallery_upload_to(instance, filename):
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    return os.path.join('animals', 'gallery', f'{uuid4().hex}.{ext}')


class AnimalPhoto(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='photos', verbose_name='Животное')
    image = models.ImageField('Фото', upload_to=animal_gallery_upload_to)
    caption = models.CharField('Подпись', max_length=200, blank=True)
    date = models.DateField('Дата', auto_now_add=True)

    class Meta:
        verbose_name = 'Фото животного'
        verbose_name_plural = 'Фото животных'
        ordering = ['-date']

    def __str__(self):
        return f'{self.animal.name} — {self.date}'


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
    # Расширенные параметры из справочника (террариум, группы/пол, возрастное кормление, разморозка и т.п.).
    # Это позволяет хранить структурированные данные без разрастания модели.
    catalog_details = models.JSONField("Расширенные детали справочника", blank=True, default=dict)

    class Meta:
        verbose_name = "Требование по уходу"
        verbose_name_plural = "Требования по уходу"

    def __str__(self):
        return f"Уход для {self.taxonomy.species}"
