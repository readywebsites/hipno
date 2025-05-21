# app/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_redirect_url(self, request):
        # After email confirmation, redirect to OTP verification
        return reverse('verify_otp')
    
    def post_login(self, request, user, *args, **kwargs):
        # Preserve user_type in session if it exists
        if 'user_type' not in request.session:
            if hasattr(user, 'doctorprofile'):
                request.session['user_type'] = 'doctor'
            elif hasattr(user, 'patientprofile'):
                request.session['user_type'] = 'patient'
        return super().post_login(request, user, *args, **kwargs)