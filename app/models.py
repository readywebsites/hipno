from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)

    # Optional
    experience = models.IntegerField(null=True, blank=True)
    clinic_address = models.TextField(null=True, blank=True)
    education = models.CharField(max_length=200, null=True, blank=True)
    availability = models.CharField(max_length=100, null=True, blank=True)
    consultation_fee = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    # Optional extended details
    reason_concerns = models.TextField(null=True, blank=True)
    concern_duration = models.CharField(max_length=100, null=True, blank=True)
    reason_now = models.TextField(null=True, blank=True)
    past_therapy = models.CharField(max_length=10, null=True, blank=True)
    therapy_reason = models.TextField(null=True, blank=True)
    past_diagnosis = models.TextField(null=True, blank=True)
    hospitalization = models.TextField(null=True, blank=True)
    current_medication = models.CharField(max_length=10, null=True, blank=True)
    medication_list = models.TextField(null=True, blank=True)
    medical_conditions = models.TextField(null=True, blank=True)
    surgeries = models.TextField(null=True, blank=True)
    substance_use = models.TextField(null=True, blank=True)
    family_history = models.TextField(null=True, blank=True)
    living_with = models.TextField(null=True, blank=True)
    support_system = models.TextField(null=True, blank=True)
    sleep = models.TextField(null=True, blank=True)
    appetite = models.TextField(null=True, blank=True)
    energy_concentration = models.TextField(null=True, blank=True)
    life_changes = models.TextField(null=True, blank=True)
    self_harm_thoughts = models.TextField(null=True, blank=True)
    suicide_attempts = models.TextField(null=True, blank=True)
    environment_safety = models.TextField(null=True, blank=True)
    therapy_goals = models.TextField(null=True, blank=True)
    consent_acknowledged = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ("manual_therapy", "Personalized Individual Therapy"),
        ("chronic_pain", "Supportive Couples Counseling"),
        ("hand_therapy", "Youth and Adolescent Counseling"),
        ("sports_therapy", "Anxiety and Depression Support"),
        ("cupping_therapy", "Stress and Anger Management"),
        ("laser_therapy", "Mindfulness and Meditation Practices"),
    ]

    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    services = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    submitted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.fname} {self.lname} - {self.services}"

class Contact(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.CharField(max_length=1000)
    date = models.DateField()
    submitted_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.fname} {self.lname}"


