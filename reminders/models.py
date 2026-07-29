from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Reminder(models.Model):
    TYPE_CHOICES = [
        ('FEEDING', 'Кормление'),
        ('VET', 'Ветеринар'),
        ('CUSTOM', 'Другое'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Ожидает'),
        ('DONE', 'Выполнено'),
        ('DISMISSED', 'Отклонено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    animal = models.ForeignKey('animals.Animal', on_delete=models.CASCADE, null=True, blank=True)
    reminder_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    source_id = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['due_date']
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'

    def __str__(self):
        return f'{self.title} — {self.due_date}'

    @property
    def is_overdue(self):
        return self.status == 'PENDING' and self.due_date < timezone.localdate()
