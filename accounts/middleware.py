import json
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import user_logged_in, user_logged_out
from .models import ActivityLog

class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        user_logged_in.connect(self.user_logged_in)
        user_logged_out.connect(self.user_logged_out)

    def user_logged_in(self, sender, request, user, **kwargs):
        self.log_action(user, 'LOGIN', request)

    def user_logged_out(self, sender, request, user, **kwargs):
        if user:
            self.log_action(user, 'LOGOUT', request)

    def log_action(self, user, action, request):
        ActivityLog.objects.create(
            user=user,
            action=action,
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
            additional_info={
                'path': request.path,
                'method': request.method
            }
        )

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    def __call__(self, request):
        response = self.get_response(request)
        return response
