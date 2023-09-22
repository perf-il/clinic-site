# Generated by Django 4.2.5 on 2023-09-18 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_remove_doctor_working_days'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')], max_length=1, unique=True, verbose_name='день недели')),
                ('doctor', models.ManyToManyField(blank=True, null=True, to='clinic.doctor', verbose_name='врач')),
            ],
            options={
                'verbose_name': 'расписание',
                'verbose_name_plural': 'расписание',
            },
        ),
    ]
