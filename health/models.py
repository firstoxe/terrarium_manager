from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class WeightLog(models.Model):
    animal = models.ForeignKey(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='weight_logs', verbose_name='Животное',
    )
    date = models.DateField('Дата', default=timezone.localdate)
    weight_g = models.FloatField('Вес (г)')
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Запись веса'
        verbose_name_plural = 'Записи веса'
        ordering = ['-date']

    def __str__(self):
        return f'{self.animal.name}: {self.weight_g}g'


class HealthRecord(models.Model):
    animal = models.ForeignKey(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='health_records', verbose_name='Животное',
    )
    date = models.DateField('Дата', default=timezone.localdate)
    reason = models.CharField('Причина', max_length=200)
    diagnosis = models.TextField('Диагноз', blank=True)
    treatment = models.TextField('Лечение', blank=True)
    vet_name = models.CharField('Ветеринар', max_length=100, blank=True)
    cost = models.DecimalField('Затраты', max_digits=10, decimal_places=2, default=0)
    next_visit_date = models.DateField('Следующий визит', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
        ordering = ['-date']

    def __str__(self):
        return f'{self.animal.name}: {self.reason}'


class SheddingLog(models.Model):
    QUALITY_CHOICES = [
        ('COMPLETE', 'Полная'),
        ('PARTIAL', 'Частичная'),
        ('PROBLEMS', 'Проблемы'),
    ]
    animal = models.ForeignKey(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='shedding_logs', verbose_name='Животное',
    )
    date = models.DateField('Дата', default=timezone.localdate)
    quality = models.CharField('Качество', max_length=20, choices=QUALITY_CHOICES, default='COMPLETE')
    notes = models.TextField('Заметки', blank=True)

    class Meta:
        verbose_name = 'Линька'
        verbose_name_plural = 'Линьки'
        ordering = ['-date']

    def __str__(self):
        return f'{self.animal.name}: {self.get_quality_display()}'
