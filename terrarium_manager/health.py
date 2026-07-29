from django.http import JsonResponse
from django.db import connection


def health_check(request):
    try:
        connection.ensure_connection()
        return JsonResponse({'status': 'ok'})
    except Exception as exc:
        return JsonResponse({'status': 'error', 'detail': str(exc)}, status=503)
