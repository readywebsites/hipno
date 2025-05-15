from django.db import models

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
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.fname} {self.lname} - {self.services}"

