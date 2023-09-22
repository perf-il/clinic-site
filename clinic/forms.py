import datetime

from django import forms
from django.forms import SelectDateWidget

from clinic.models import Order, Service, Doctor, Schedule
from clinic.utilits import get_week_days


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({

                'class': 'form-control',
                'autocomplete': 'off'
            })


class OrderForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Order
        fields = ('doctor', 'service', 'data', 'time')
        widgets = {
            'data': SelectDateWidget()
        }

    def clean(self):
        if not self._errors:
            cleaned_data = super(OrderForm, self).clean()
            doctor = cleaned_data.get('doctor')
            service = cleaned_data.get('service')
            data = cleaned_data.get('data')
            time = cleaned_data.get('time')
            orders = Order.objects.filter(data=data, doctor=doctor, status='IW').order_by('data')
            schedule = [int(w_day.day) for w_day in Schedule.objects.filter(doctor=doctor).order_by('day')]
            start_work = datetime.time(8)
            end_work = datetime.time(20)

            # проверка полей doctor и service на совместимость
            if doctor.direction != service.direction:
                raise forms.ValidationError('Доктор не оказывает выбранную услугу.')

            # проверка даты - дата должна быть не раньше чем завтрашний день
            if data < datetime.date.today() + datetime.timedelta(days=1):
                raise forms.ValidationError('Нельзя записаться на прошедшую или текущую дату')

            # проверка расписания врача
            if data.weekday() not in schedule:
                raise forms.ValidationError(f'Рабочие дни врача - {get_week_days(schedule)}')

            # проверка поле time - время должно укладываться в рабочие часы
            # и быть свободным (время существующей записи + час)
            all_time = [cursor.time for cursor in orders.exclude(status='CN')]
            if start_work <= time <= end_work:
                if not all_time or min(all_time) >= datetime.time(start_work.hour + 1):
                    next_free_time = start_work
                else:
                    next_free_time = datetime.time(start_work.hour + 1)
                    for cur_time in all_time:
                        if datetime.time(cur_time.hour - 1, cur_time.minute) < next_free_time:
                            next_free_time = datetime.time(cur_time.hour + 1, cur_time.minute)
                if next_free_time >= end_work:
                    raise forms.ValidationError('Записи на этот день нет. Выберите другую дату')
                for cur_time in all_time:
                    if cur_time <= time < datetime.time(cur_time.hour + 1, cur_time.minute):
                        raise forms.ValidationError(f'Время {time.strftime("%H:%M")} '
                                                    f'уже занято.Ближайшее свободное время '
                                                    f'{next_free_time.strftime("%H:%M")}')
            else:
                raise forms.ValidationError(f'Время работы клиники '
                                            f'с {start_work.strftime("%H:%M")} до {end_work.strftime("%H:%M")}')
            return cleaned_data

