from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class FeedingSchedule(models.Model):
    animal = models.OneToOneField(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='feeding_schedule', verbose_name='Животное',
    )
    interval_days = models.PositiveIntegerField('Интервал (дней)', default=7)
    food_type = models.CharField('Тип корма', max_length=100)
    amount = models.PositiveIntegerField('Количество', default=1)
    is_active = models.BooleanField('Активно', default=True)
    last_fed = models.DateTimeField('Последнее кормление', null=True, blank=True)

    class Meta:
        verbose_name = 'Расписание кормления'
        verbose_name_plural = 'Расписания кормления'

    def __str__(self):
        return f'{self.animal.name}: каждые {self.interval_days} дн.'

    @property
    def next_feed_date(self):
        if not self.last_fed:
            return timezone.now()
        from datetime import timedelta
        return self.last_fed + timedelta(days=self.interval_days)

    @property
    def is_overdue(self):
        return self.is_active and self.next_feed_date <= timezone.now()

    @property
    def is_due_today(self):
        if not self.is_active:
            return False
        next_date = self.next_feed_date.date()
        return next_date <= timezone.localdate()


class FeedingLog(models.Model):
    animal = models.ForeignKey(
        'animals.Animal', on_delete=models.CASCADE,
        related_name='feeding_logs', verbose_name='Животное',
    )
    date = models.DateTimeField('Дата кормления', default=timezone.now)
    food_type = models.CharField('Тип корма', max_length=100)
    amount = models.PositiveIntegerField('Количество', default=1)
    notes = models.TextField('Заметки', blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True,
        verbose_name='Автор',
    )
    action = models.OneToOneField(
        'animals.Action', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='feeding_log',
    )

    class Meta:
        verbose_name = 'Запись кормления'
        verbose_name_plural = 'Записи кормления'
        ordering = ['-date']

    def __str__(self):
        return f'{self.animal.name} — {self.food_type} ({self.date:%d.%m.%Y})'
