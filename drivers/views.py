# drivers/views.py
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User  
from django.db import models
import logging

from .forms import BookingForm, ReviewForm, ContactForm
from .models import Review

logger = logging.getLogger(__name__)

def home(request):
    booking_form = BookingForm()
    contact_form = ContactForm()
    reviews = Review.objects.filter(is_published=True)

    return render(request, 'drivers/home.html', {
        'booking_form': booking_form,
        'contact_form': contact_form,
        'review_form': ReviewForm(),
        'reviews': reviews,
    })


def booking(request):
    if request.method != 'POST':
        return redirect('drivers:home')

    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        
        # Attach the booking to your admin/first user behind the scenes
        default_user = User.objects.first()
        if default_user:
            booking.user = default_user
        else:
            booking.user = User.objects.create_user(username='system_guest')
            
        booking.save()

        # 🛡️ PROTECTED EMAIL BLOCK (Indented exactly 8 spaces)
        try:
            send_mail(
                subject='New lesson booking request',
                message=(
                    f"New booking request from {booking.name}\n"
                    f"Email: {booking.email}\n"
                    f"Phone: {booking.phone or 'No phone provided'}\n"
                    f"Date: {booking.date}\n"
                    f"Time: {booking.time}\n"
                    f"Message: {booking.message or 'No message provided'}"
                ),
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=['driversdenlearning@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            # If Gmail connection fails, it logs the error instead of crashing the site
            logger.error(f"Email failed to send: {e}")

        messages.success(request, 'Your lesson booking has been received. Thank you!')
        return redirect('drivers:home')

    return render(request, 'drivers/home.html', {
        'booking_form': form,
        'contact_form': ContactForm(),
        'review_form': ReviewForm(),
        'reviews': Review.objects.filter(is_published=True),
    })


def submit_review(request):
    if request.method != 'POST':
        return redirect('drivers:home')

    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        
        default_user = User.objects.first()
        if default_user:
            review.user = default_user
        else:
            review.user = User.objects.create_user(username='system_guest')
            
        review.save()
        messages.success(request, 'Your review has been published successfully.')
    else:
        messages.error(request, 'Please enter a valid review.')

    return redirect('drivers:home')


def contact(request):
    if request.method != 'POST':
        return redirect('drivers:home')

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_msg = form.save()

        # 🛡️ PROTECTED EMAIL BLOCK FOR CONTACT
        try:
            send_mail(
                subject=f"New Contact Us Message: {contact_msg.subject}",
                message=(
                    f"You received a new contact submission:\n\n"
                    f"Name: {contact_msg.name}\n"
                    f"Email: {contact_msg.email}\n\n"
                    f"Message:\n{contact_msg.message}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['driversdenlearning@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Contact email failed to send: {e}")

        messages.success(request, 'Your message has been sent successfully. Thank you!')
        return redirect('drivers:home')

    return render(request, 'drivers/home.html', {
        'booking_form': BookingForm(),
        'contact_form': form,
        'review_form': ReviewForm(),
        'reviews': Review.objects.filter(is_published=True),
    })
