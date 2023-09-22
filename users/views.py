from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, TemplateView

from clinic.models import Order
from users.forms import UserRegisterForm, UserProfileForm, UserForgotPasswordForm, UserSetNewPasswordForm
from users.models import User
from users.services import send_email_activate


def private_cabinet(request, pk):
    if request.user.is_authenticated and request.user.pk == pk:
        current_user = User.objects.get(pk=pk)
        user_orders = Order.objects.filter(user=current_user).order_by('data', 'time')
        active_orders = user_orders.filter(status='IW')
        closed_orders = user_orders.filter(status='CL')
        canceled_orders = user_orders.filter(status='CN')
        template = 'users/private_cabinet.html'
        context = {
            'title': f'Личный кабинет {current_user}',
            'current_user': current_user,
            'user_orders': user_orders,
            'active_orders': active_orders,
            'closed_orders': closed_orders,
            'canceled_orders': canceled_orders,

        }
    else:
        return redirect('users:login')

    return render(request, template, context)


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

    def form_valid(self, form):
        if form.is_valid:
            fields = form.save()
            send_email_activate((fields.email,), fields.pk)
        return super().form_valid(form)


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:private_cabinet', kwargs={'pk': self.request.user.pk})


def wait_confirm_email(request):
    context = {
        'title': 'Верификация пользователя'
    }

    return render(request, 'users/wait_confirm_email.html', context)


class ConfirmPage(TemplateView):
    template_name = 'users/confirmed_email.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        pk = context_data['pk']
        if User.objects.filter(pk=pk).exists():
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
        return context_data


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'users/email/password_subject_reset_mail.txt'
    email_template_name = 'users/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetDoneView(SuccessMessageMixin, PasswordResetDoneView):
    template_name = "users/user_password_reset_done.html"
    title = "Пароль сброшен"


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context