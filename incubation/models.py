from django.db import models
from django.utils import timezone


class BreedingPair(models.Model):
    male = models.ForeignKey(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='breeding_as_male', verbose_name='Самец',
    )
    female = models.ForeignKey(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='breeding_as_female', verbose_name='Самка',
    )
    start_date = models.DateField('Дата начала', default=timezone.localdate)
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Пара для разведения'
        verbose_name_plural = 'Пары для разведения'

    def __str__(self):
        return f'{self.male.name} × {self.female.name}'


class Clutch(models.Model):
    pair = models.ForeignKey(BreedingPair, on_delete=models.CASCADE, related_name='clutches')
    lay_date = models.DateField('Дата кладки')
    egg_count = models.PositiveIntegerField('Кол-во яиц')
    infertile_count = models.PositiveIntegerField('Нefertil', default=0)

    class Meta:
        verbose_name = 'Кладка'
        verbose_name_plural = 'Кладки'

    def __str__(self):
        return f'Кладка {self.lay_date} ({self.egg_count} яиц)'


class IncubationRecord(models.Model):
    clutch = models.OneToOneField(Clutch, on_delete=models.CASCADE, related_name='incubation')
    start_date = models.DateField('Начало инкубации')
    expected_hatch = models.DateField('Ожидаемое вылупление')
    temperature = models.FloatField('Температура °C', null=True, blank=True)
    humidity = models.FloatField('Влажность %', null=True, blank=True)

    class Meta:
        verbose_name = 'Инкубация'
        verbose_name_plural = 'Инкубации'

    @property
    def days_remaining(self):
        return (self.expected_hatch - timezone.localdate()).days


class HatchRecord(models.Model):
    incubation = models.ForeignKey(IncubationRecord, on_delete=models.CASCADE, related_name='hatches')
    hatch_date = models.DateField('Дата вылупления')
    hatched_count = models.PositiveIntegerField('Вылупилось')
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Запись вылупления'
        verbose_name_plural = 'Записи вылупления'
