from django.conf import settings


def site_imprint(request):
    return {
        'SITE_IMPRINT': settings.SITE_IMPRINT,
    }

