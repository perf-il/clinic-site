from datetime import datetime

from celery import shared_task

from clinic.models import Order


@shared_task
def check_status_order():
    """Проверка даты заказов, находящихся в ожидании"""
    active_orders = Order.objects.filter(status='IW')

    for order in active_orders:

        if order.data <= datetime.now().date():
            if order.time <= datetime.now().time():
                order.status = 'CL'
                order.save()
