from django.conf import settings


def severus(request):
    return {
        'ENVIRONMENT': settings.ENVIRONMENT,
    }
