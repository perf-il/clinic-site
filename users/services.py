from django.core.mail import send_mail

from config import settings


def send_email_activate(email, pk):
    send_mail(
        'Активация профиля',
        f'Добрый день.\n'
        f'Для активации профиля на сайте перейдите по ссылке http://{settings.IP_ADDRESS}/users/confirm_email/{pk}',
        settings.EMAIL_HOST_USER,
        email
    )
