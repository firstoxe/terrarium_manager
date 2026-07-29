from django.conf import settings
from django.http import FileResponse


def service_worker(request):
    response = FileResponse(
        open(settings.BASE_DIR / 'static' / 'sw.js', 'rb'),
        content_type='application/javascript',
    )
    response['Service-Worker-Allowed'] = '/'
    return response
