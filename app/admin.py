from django.contrib import admin
from .models import Appointment, Contact, DoctorProfile, PatientProfile

admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'services', 'date',)
    search_fields = ('fname', 'lname', 'email')

@admin.register(Contact)
class contactAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'message', 'date', 'submitted_at')
    search_fields = ('fname', 'lname', 'email')
