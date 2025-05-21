from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointment, Contact, DoctorProfile, PatientProfile
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.contrib.auth import authenticate, login
from django.contrib import messages
import random
from datetime import datetime  # Add this at the top of your views.py
from django.conf import settings

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
            messages.error(request, "OTP expired or not generated. Please request a new OTP.")
            return redirect('account_email_verification_sent')
            
        if user_otp == session_otp:
            # Check user type from session (set during signup)
            user_type = request.session.get('user_type')
            
            if user_type == 'doctor':
                return redirect('doctor_detail')
            elif user_type == 'patient':
                return redirect('patient_detail')
            else:
                # Fallback if user_type not set
                return redirect('account_login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    
    return render(request, 'signup/verify_otp.html')

def doctor_detail(request):
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
        return redirect('success')  # or dashboard

    return render(request, 'signup/doctor_details.html')


def patient_detail(request):
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
        return redirect('success')  # or dashboard

    return render(request, 'signup/patient_details.html')


# -------------------- SIGNUP DOCTOR --------------------
def signup_doctor(request):
    if request.method == 'POST':
        verification_method = request.POST.get('verification_method')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        request.session['user_type'] = 'doctor'

        if verification_method == 'email' and email:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['email'] = email

            send_mail(
                subject='Doctor OTP',
                message=f'Your OTP is {otp}',
                from_email='fatemadhalech16@gmail.com',  # change to your .env value
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'signup/verify_otp.html', {'email': email})

        elif verification_method == 'phone' and phone:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['phone'] = phone
            print(f"Doctor OTP sent to {phone}: {otp}")
            return render(request, 'signup/verify_otp.html', {'phone': phone})

    return render(request, 'signup/doctor.html')

def signup_patient(request):
    if request.method == 'POST':
        verification_method = request.POST.get('verification_method')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        request.session['user_type'] = 'patient'

        if verification_method == 'email' and email:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['email'] = email

            send_mail(
                subject='Patient OTP',
                message=f'Your OTP is {otp}',
                from_email='fatemadhalech16@gmail.com',  # use your email
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'signup/verify_otp.html', {'email': email})

        elif verification_method == 'phone' and phone:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            request.session['phone'] = phone
            print(f"Patient OTP sent to {phone}: {otp}")
            return render(request, 'signup/verify_otp.html', {'phone': phone})

    return render(request, 'signup/patient.html')


# -------------------- SIGNIN DOCTOR --------------------

def signin_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin/doctor.html', {'error': 'Invalid credentials'})
    
    return render(request, 'signin/doctor.html')



# -------------------- SIGNIN PATIENT --------------------
def signin_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin/patient.html', {'error': 'Invalid credentials'})
    
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
