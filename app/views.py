from django.shortcuts import render
from django.http import JsonResponse
from .models import Appointment, contact
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from datetime import date

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
        contact_obj = contact.objects.create(
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
