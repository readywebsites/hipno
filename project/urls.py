"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from app import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog-single/', views.blog_single, name='blog_single'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('case-study/', views.case_study, name='case_study'),
    path('case-study-single/', views.case_study_single, name='case_study_single'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('image-gallery/', views.image_gallery, name='image_gallery'),
    path('index-slider/', views.index_slider, name='index_slider'),
    path('index-video/', views.index_video, name='index_video'),
    path('pricing/', views.pricing, name='pricing'),
    path('service-single/', views.service_single, name='service_single'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('team-single/', views.team_single, name='team_single'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('video-gallery/', views.video_gallery, name='video_gallery'),
    path('404/', views.error_404, name='error_404'),
    path('submit-appointment/', views.appointment_submit, name='appointment_submit'),
    path('submit-contact/', views.contact_submit, name='contact_submit'),
    path('signup/doctor/', views.signup_doctor, name='signup_doctor'),
    path('signup/patient/', views.signup_patient, name='signup_patient'),
    path('signin/doctor/', views.signin_doctor, name='signin_doctor'),
    path('signin/patient/', views.signin_patient, name='signin_patient'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('signup/doctor_detail/', views.doctor_detail, name='doctor_detail'),
    path('signup/patient_detail/', views.patient_detail, name='patient_detail'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('create-password/', views.create_password, name='create_password'),
    path('test-doc/', views.test_template),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]

from django.conf import settings

from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)