from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'services', 'date',)
    search_fields = ('fname', 'lname', 'email')

