from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointment, Contact, DoctorProfile, PatientProfile
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
from datetime import datetime  # Add this at the top of your views.py
from django.conf import settings
from django.contrib.auth.models import User

def profile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    try:
        profile = DoctorProfile.objects.get(user=request.user)
        profile_type = 'doctor'
    except DoctorProfile.DoesNotExist:
        try:
            profile = PatientProfile.objects.get(user=request.user)
            profile_type = 'patient'
        except PatientProfile.DoesNotExist:
            messages.error(request, 'Profile not found')
            return redirect('index')
    
    return render(request, 'profile.html', {
        'profile': profile,
        'profile_type': profile_type
    })

def logout_view(request):
    logout(request)
    return redirect('index')

def test_template(request):
    return render(request, 'signup/doctor_detail.html')

def resend_otp(request):
    if 'otp' in request.session:
        del request.session['otp']
    return redirect('send_otp')

def send_otp(request):
    # Generate a random 6-digit OTP
    otp = random.randint(100000, 999999)
    request.session['otp'] = str(otp)
    request.session['otp_created_time'] = str(datetime.now())
    
    # Send email with the OTP
    send_mail(
        'Your OTP for verification',
        f'Your OTP is: {otp}',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=False,
    )
    messages.info(request, 'OTP sent to your email!')
    return redirect('verify_otp')
  

def forgot_password(request):
    return render(request, 'forgot_password.html')

def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")

        if not session_otp:
            messages.error(request, "OTP expired. Please try again.")
            return redirect('resend_otp')

        if user_otp == session_otp:
            return redirect('create_password')
        else:
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, 'signup/verify_otp.html')

def create_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email = request.session.get("email")
        user_type = request.session.get("user_type")

        if password != confirm_password:
            messages.error(request, "Passwords don't match")
            return render(request, 'signup/create_password.html')

        if email and password:
            if User.objects.filter(email=email).exists():
                messages.error(request, "User already exists.")
                return redirect('signin_patient' if user_type == 'patient' else 'signin_doctor')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password
            )
            login(request, user)
            return redirect('doctor_detail' if user_type == 'doctor' else 'patient_detail')

    return render(request, 'signup/create_password.html')

def doctor_detail(request):
    if not request.user.is_authenticated:
        return redirect('signin_doctor')

    if request.method == "POST":
        DoctorProfile.objects.create(
            user=request.user,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            specialization=request.POST['specialization'],
            license_number=request.POST['license_number'],
            experience=request.POST.get('experience'),
            clinic_address=request.POST.get('clinic_address'),
            education=request.POST.get('education'),
            availability=request.POST.get('availability'),
            consultation_fee=request.POST.get('consultation_fee'),
            bio=request.POST.get('bio'),
        )
        return redirect('index')

    return render(request, 'signup/doctor_detail.html')

def patient_detail(request):
    if not request.user.is_authenticated:
        return redirect('signin_patient')

    if request.method == "POST":
        PatientProfile.objects.create(
            user=request.user,
            name=request.POST['name'],
            email=request.POST['email'],
            phone_number=request.POST['phonenumber'],
            dob=request.POST.get('dob'),
            emergency_contact=request.POST.get('emergency_contact'),
            gender=request.POST.get('gender'),
            age=request.POST.get('age'),
            reason_concerns=request.POST.get('reason_concerns'),
            concern_duration=request.POST.get('concern_duration'),
            reason_now=request.POST.get('reason_now'),
            past_therapy=request.POST.get('past_therapy'),
            therapy_reason=request.POST.get('therapy_reason'),
            past_diagnosis=request.POST.get('past_diagnosis'),
            hospitalization=request.POST.get('hospitalization'),
            current_medication=request.POST.get('current_medication'),
            medication_list=request.POST.get('medication_list'),
            medical_conditions=request.POST.get('medical_conditions'),
            surgeries=request.POST.get('surgeries'),
            substance_use=request.POST.get('substance_use'),
            family_history=request.POST.get('family_history'),
            living_with=request.POST.get('living_with'),
            support_system=request.POST.get('support_system'),
            sleep=request.POST.get('sleep'),
            appetite=request.POST.get('appetite'),
            energy_concentration=request.POST.get('energy_concentration'),
            life_changes=request.POST.get('life_changes'),
            self_harm_thoughts=request.POST.get('self_harm_thoughts'),
            suicide_attempts=request.POST.get('suicide_attempts'),
            environment_safety=request.POST.get('environment_safety'),
            therapy_goals=request.POST.get('therapy_goals'),
            consent_acknowledged=request.POST.get('consent_acknowledged'),
        )
        return redirect('index')

    return render(request, 'signup/patient_detail.html')

# -------------------- SIGNUP DOCTOR --------------------
def signup_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists')
            return redirect('signin_doctor')

        request.session['email'] = email
        request.session['user_type'] = 'doctor'
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp

        send_mail(
            subject='Doctor OTP Verification',
            message=f'Your OTP is: {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return redirect('verify_otp')

    return render(request, 'signup/doctor.html')

def signup_patient(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists')
            return redirect('signin_patient')

        request.session['email'] = email
        request.session['user_type'] = 'patient'
        otp = str(random.randint(100000, 999999))
        request.session['otp'] = otp

        send_mail(
            subject='Patient OTP Verification',
            message=f'Your OTP is: {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return redirect('verify_otp')

    return render(request, 'signup/patient.html')


# -------------------- SIGNIN DOCTOR --------------------

def signin_doctor(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, 'Invalid credentials')
    
    return render(request, 'signin/doctor.html')



# -------------------- SIGNIN PATIENT --------------------
def signin_patient(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, 'Invalid credentials')
    
    return render(request, 'signin/patient.html')


def book_appointment_view(request):
    today = date.today().isoformat()
    return render(request, "book_appointment.html", {"today_date": today})

@csrf_exempt
def appointment_submit(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        services = request.POST.get("services")
        date = request.POST.get("date")

        # Save to model
        appointment = Appointment.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            services=services,
            date=date
        )

        # Email to user
        send_mail(
            subject="Your appointment request is received",
            message=f"Hi {fname},\n\nYour form has been submitted successfully. We'll get back to you shortly.",
            from_email="fatemadhalech16@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )

        # Email to admin
        send_mail(
            subject="New appointment inquiry",
            message=f"New inquiry from {fname} {lname}\nEmail: {email}\nPhone: {phone}\nService: {services}\nDate: {date}",
            from_email="fatemadhalech16@gmail.com",
            recipient_list=["fatemadhalech16@gmail.com"],
            fail_silently=False,
        )

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

@csrf_exempt
def contact_submit(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        date = request.POST.get("date")

        # Save form data
        contact_obj = Contact.objects.create(
            fname=fname,
            lname=lname,
            email=email,
            phone=phone,
            message=message,
            date=date
        )

        # Email to user
        send_mail(
            subject="Your appointment request is received",
            message=f"Hi {fname},\n\nYour enquiry has been submitted successfully. We'll get back to you shortly.",
            from_email="fatemadhalech16@gmail.com",
            recipient_list=[email],
            fail_silently=True,
        )

        # Email to admin
        send_mail(
            subject="New appointment inquiry",
            message=f"New inquiry from {fname} {lname}\nEmail: {email}\nPhone: {phone}\nMessage: {message}\nDate: {date}",
            from_email="fatemadhalech16@gmail.com",
            recipient_list=["fatemadhalech16@gmail.com"],
            fail_silently=True,
        )

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def blog_single(request):
    return render(request, 'blog-single.html')

def book_appointment(request):
    return render(request, 'book-appointment.html')

def case_study(request):
    return render(request, 'case-study.html')

def case_study_single(request):
    return render(request, 'case-study-single.html')

def contact(request):
    return render(request, 'contact.html')

def faqs(request):
    return render(request, 'faqs.html')

def image_gallery(request):
    return render(request, 'image-gallery.html')

def index_slider(request):
    return render(request, 'index-slider.html')

def index_video(request):
    return render(request, 'index-video.html')

def pricing(request):
    return render(request, 'pricing.html')

def service_single(request):
    return render(request, 'service-single.html')

def services(request):
    return render(request, 'services.html')

def team(request):
    return render(request, 'team.html')

def team_single(request):
    return render(request, 'team-single.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def video_gallery(request):
    return render(request, 'video-gallery.html')

def error_404(request):
    return render(request, '404.html')
