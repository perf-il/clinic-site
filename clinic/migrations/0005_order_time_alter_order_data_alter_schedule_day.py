# Generated by Django 4.2.5 on 2023-09-19 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0004_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.TimeField(blank=True, null=True, verbose_name='время'),
        ),
        migrations.AlterField(
            model_name='order',
            name='data',
            field=models.DateField(verbose_name='дата'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=1, unique=True, verbose_name='день недели'),
        ),
    ]
