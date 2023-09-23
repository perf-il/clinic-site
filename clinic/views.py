from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from clinic.forms import OrderForm
from clinic.models import Doctor, Service, Direction, Schedule, Order
from clinic.services import send_email_new_order, send_email_update_order, send_email_delete_order
from config import settings


def home(request):
    print(settings.DEBUG)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('comment')
        print(f'Новое сообщение от {name}: {message}\nТелефон: {phone}\nE-mail: {email}')

    doctors = Doctor.objects.all().order_by('?')[:3]
    discounts = Service.objects.filter(discount__lt='1').order_by('?')[:3]
    context = {
        'title': 'Главная страница',
        'doctors': doctors,
        'discounts': discounts,
    }

    return render(request, 'clinic/home.html', context)


def discount(request):
    discount_services = Service.objects.filter(discount__lt='1')

    context = {
        'discount_services': discount_services,
        'title': 'Скидки и акции'
    }

    return render(request, 'clinic/discount.html', context)


def services(request, pk):
    all_services = Service.objects.filter(direction=pk)
    direction_name = Direction.objects.get(pk=pk).title
    context = {
        'all_services': all_services,
        'direction_name': direction_name,
        'title': 'Скидки и акции'
    }

    return render(request, 'clinic/services.html', context)


def schedule(request):
    doctors = Doctor.objects.all()
    schedules = Schedule.objects.all().order_by('day')

    context = {
        'doctors': doctors,
        'schedules': schedules,
        'title': 'Расписание'
    }

    return render(request, 'clinic/schedule.html', context)


class DoctorsListView(generic.ListView):
    model = Doctor
    extra_context = {
        'title': 'Список врачей'
    }


class DoctorDetailView(generic.DetailView):
    model = Doctor

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        context_data['schedule'] = Schedule.objects.all().order_by('day')
        return context_data


class DirectionsListView(generic.ListView):
    model = Direction
    extra_context = {
        'title': 'Список категорий услуг'
    }


class ServicesListView(generic.ListView):
    model = Service
    extra_context = {
        'title': 'Список услуг'
    }


class ServicesDetailView(generic.DetailView):
    model = Service

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = self.get_object()
        return context_data


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        if form.is_valid():
            fields = form.save(commit=False)
            fields.user = self.request.user
            fields.price = \
                Service.objects.get(pk=fields.service.pk).price * Service.objects.get(pk=fields.service.pk).discount
            email_list = [self.request.user.email]
            send_email_new_order(email_list, fields)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:private_cabinet', kwargs={'pk': self.request.user.pk})


class OrderUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderForm
    extra_context = {
        'title': 'Редактировать запись'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        if self.object.user != self.request.user:
            raise Http404('Нет прав доступа')
        return self.object

    def get_success_url(self):
        return reverse('users:private_cabinet', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        if form.is_valid():
            fields = form.save(commit=False)
            email_list = [self.request.user.email]
            send_email_update_order(email_list, fields)
        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Order
    extra_context = {
        'title': 'Удалить запись'
    }

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        if self.object.user != self.request.user:
            raise Http404('Нет прав доступа')
        return self.object

    def get_success_url(self):
        return reverse('users:private_cabinet', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        email_list = [self.request.user.email]
        obj = self.get_object()
        send_email_delete_order(email_list, obj)
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
