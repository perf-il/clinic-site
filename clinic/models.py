from django.db import models
from users.models import User, NULLABLE

DAYS_OF_WEEK = (
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
    )

STATUS_OF_ORDER = (
        ('IW', 'Waiting'),
        ('CL', 'Closed'),
        ('CN', 'Canceled'),
    )


class Direction(models.Model):
    title = models.CharField(max_length=255, verbose_name='наименование')
    preview = models.ImageField(upload_to='direction/preview', default='avatars/avatar.png',
                                verbose_name='изображение', **NULLABLE)

    class Meta:
        verbose_name = 'направление'
        verbose_name_plural = 'направления'

    def __str__(self):
        return self.title


class Service(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='направление')
    title = models.CharField(max_length=255, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    price = models.FloatField(verbose_name='цена')
    preview = models.ImageField(upload_to='services/preview', default='avatars/avatar.png',
                                verbose_name='изображение', **NULLABLE)
    discount = models.FloatField(default=1, verbose_name='скидка')

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def __str__(self):
        return self.title


class Doctor(models.Model):

    name = models.CharField(max_length=255, verbose_name='имя')
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, verbose_name='направление', **NULLABLE)
    preview = models.ImageField(upload_to='avatars/', default='avatars/avatar-round.png',
                                verbose_name='изображение', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    class Meta:
        verbose_name = 'врач'
        verbose_name_plural = 'врачи'

    def __str__(self):
        return self.name


class Schedule(models.Model):

    day = models.CharField(max_length=1, choices=DAYS_OF_WEEK, unique=True, verbose_name='день недели', )
    doctor = models.ManyToManyField(Doctor, verbose_name='врач', **NULLABLE)

    class Meta:
        verbose_name = 'расписание'
        verbose_name_plural = 'расписание'

    def __str__(self):
        return self.day


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='клиент')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, verbose_name='врач', **NULLABLE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='услуга')
    data = models.DateField(verbose_name='дата')
    time = models.TimeField(verbose_name='время', **NULLABLE)
    data_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_OF_ORDER, default='IW', verbose_name='статус')
    price = models.FloatField(verbose_name='цена', **NULLABLE)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def delete(self, *args, **kwargs):
        self.status = 'CN'
        self.save()

    def __str__(self):
        return f'{self.data} - {self.service} - {self.user}'
