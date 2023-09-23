from django.core.management import BaseCommand

from config import settings
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=settings.SUPER_USER_MAIL,
            first_name=settings.SUPER_USER_FIRSTNAME,
            last_name=settings.SUPER_USER_LASTNAME,
            is_staff=True,
            is_superuser=True,
            is_active=True
        )

        user.set_password(settings.SUPER_USER_PASSWORD)
        user.save()
