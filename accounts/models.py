from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    is_approved = models.BooleanField(
        _('Approved'),
        default=False,
        help_text=_('Designates whether the user has been approved.')
    )
    phone = models.CharField(
        _('Phone number'),
        max_length=20,
        blank=True,
        help_text=_('Format: +79991234567')
    )
    registration_date = models.DateTimeField(
        _('Registration date'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.get_full_name() or self.username


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Вход в систему'),
        ('LOGOUT', 'Выход из системы'),
        ('PASSWORD_CHANGE', 'Смена пароля'),
        ('PROFILE_UPDATE', 'Обновление профиля'),
        ('REGISTER', 'Регистрация'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    additional_info = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Лог активности'
        verbose_name_plural = 'Логи активности'

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.timestamp}"
