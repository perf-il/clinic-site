# Generated by Django 4.2.5 on 2023-09-20 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0005_order_time_alter_order_data_alter_schedule_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='data_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
