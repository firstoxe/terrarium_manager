from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import User


@receiver(post_save, sender=User)
def notify_admins_on_registration(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        # Отправка email администраторам
        subject = 'Новая регистрация на сайте'
        message = render_to_string('accounts/emails/new_user_admin_email.txt', {
            'user': instance,
            'admin_url': f"{settings.SITE_URL}/admin/accounts/user/{instance.id}/change/"
        })

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[a[1] for a in settings.ADMINS],
            fail_silently=True
        )
