from django.urls import path

from clinic.apps import ClinicConfig
from clinic import views as my_view


app_name = ClinicConfig.name

urlpatterns = [
    path('', my_view.home, name='home'),
    path('discount', my_view.discount, name='discount'),

    path('doctors', my_view.DoctorsListView.as_view(), name='all_doctors'),
    path('doctor/<int:pk>', my_view.DoctorDetailView.as_view(), name='doctor'),

    path('directions', my_view.DirectionsListView.as_view(), name='all_directions'),

    path('services', my_view.ServicesListView.as_view(), name='all_services'),
    path('services/<int:pk>', my_view.ServicesDetailView.as_view(), name='service'),
    path('services/direction/<int:pk>', my_view.services, name='service_dir'),

    path('schedule', my_view.schedule, name='schedule'),

    path('order/create', my_view.OrderCreateView.as_view(), name='order_create'),
    path('order/update/<int:pk>', my_view.OrderUpdateView.as_view(), name='order_update'),
    path('order/delete/<int:pk>', my_view.OrderDeleteView.as_view(), name='order_delete'),
]
