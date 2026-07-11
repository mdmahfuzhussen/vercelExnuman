# drivers/views.py
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User  # Needed to satisfy database constraints
from django.db import models

from .forms import BookingForm, ReviewForm, ContactForm
from .models import Review

from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

# Inside your booking submission view:
try:
    send_mail(
        'New Lesson Booking',
        'Here is the booking information...',
        'mdmahufuzmahi@gmail.com',
        ['target_email@gmail.com'],
        fail_silently=False, # Set to False inside the try block to log it properly
    )
except Exception as e:
    # This prevents the 500 error! The website keeps running even if the email fails.
    logger.error(f"Email failed to send: {e}")


def home(request):
    # Standard clean form since users no longer log in
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
        
        # Since login is removed, we attach the booking to your admin/first user 
        # so the database doesn't throw a "null constraint" error.
        default_user = User.objects.first()
        if default_user:
            booking.user = default_user
        else:
            # Fallback placeholder if no users exist in the system yet
            booking.user = User.objects.create_user(username='system_guest')
            
        booking.save()

        # Sends the details straight to your email inbox
        send_mail(
            subject='New lesson booking request',
            message=(
                f"New booking request from {booking.name}\n"
                f"Email: {booking.email}\n"
                f"Date: {booking.date}\n"
                f"Time: {booking.time}\n"
                f"Message: {booking.message or 'No message provided'}"
            ),
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=['mdmahufuzmahi@gmail.com'],
            fail_silently=False,
        )

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
        
        # Attaches the review to your admin/first user behind the scenes
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


# Add this to the bottom of drivers/models.py
def contact(request):
    if request.method != 'POST':
        return redirect('drivers:home')

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_msg = form.save()

        # Send the contact form submission directly to your email
        send_mail(
            subject=f"New Contact Us Message: {contact_msg.subject}",
            message=(
                f"You received a new contact submission:\n\n"
                f"Name: {contact_msg.name}\n"
                f"Email: {contact_msg.email}\n\n"
                f"Message:\n{contact_msg.message}"
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=['mdmahufuzmahi@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully. Thank you!')
        return redirect('drivers:home')

    return render(request, 'drivers/home.html', {
        'booking_form': BookingForm(),
        'contact_form': form,
        'review_form': ReviewForm(),
        'reviews': Review.objects.filter(is_published=True),
    })
