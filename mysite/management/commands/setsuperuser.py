from scraper.models import Service
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in get_user_model().objects.filter(username__in=args):
            print user.username
            user.is_superuser = True
            user.is_staff = True
            user.save()
