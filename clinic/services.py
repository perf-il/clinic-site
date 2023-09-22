from django.core.mail import send_mail

from clinic.models import Order
from config import settings


def send_email_new_order(email, order: Order):
    send_mail(
        'Новая запись в клинику компьютерной диагностики',
        f'Добрый день.\n\n'
        f'Вы записались на услугу {order.service} к доктору {order.doctor}\n'
        f'Дата и время заказа: {order.time} {order.data}\n'
        f'Стоимость заказа (с учетом скидки): {order.price}$\n\n'
        f'Благодарим вас за обращение и ждем вас. Хорошего вам дня.',
        settings.EMAIL_HOST_USER,
        email
    )


def send_email_update_order(email, order: Order):
    send_mail(
        'Изменение записи в клинику компьютерной диагностики',
        f'Добрый день.\n\n'
        f'Вы внесли изменения в свою запись в нашу клинику.\n'
        f'Теперь вы записаны на услугу {order.service} к доктору {order.doctor}\n'
        f'Дата и время заказа: {order.time} {order.data}\n'
        f'Стоимость заказа (с учетом скидки): {order.price}$\n\n'
        f'Благодарим вас за обращение и ждем вас. Хорошего вам дня.',
        settings.EMAIL_HOST_USER,
        email
    )


def send_email_delete_order(email, order: Order):
    send_mail(
        'Отмена записи в клинику компьютерной диагностики',
        f'Добрый день.\n\n'
        f'Вы отменили свою на услугу {order.service} к доктору {order.doctor}.\n'
        f'Вы были записаны на {order.time} {order.data}\n\n'
        f'Ждем вас в следующий раз. Хорошего вам дня.',
        settings.EMAIL_HOST_USER,
        email
    )
