from django.contrib import admin

from clinic.models import Direction, Doctor, Service, Order, Schedule


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'direction', 'description', )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'direction', 'title', 'description', 'price', 'discount',)
    list_filter = ('direction',)
    search_fields = ('title', 'description',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'doctor', 'service', 'price', 'data', 'time', 'status',)
    list_filter = ('user', 'doctor', 'service', 'data', 'status',)
    search_fields = ('user', 'doctor', 'service',)


@admin.register(Schedule)
class DScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'day',)
