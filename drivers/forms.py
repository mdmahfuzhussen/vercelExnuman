from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, ContactMessage, Review


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'placeholder': 'Username',
    }))
    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(required=False, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        # 1. Added 'phone' to the tracking fields list
        fields = ['name', 'email', 'phone', 'date', 'time', 'message']
        
        # 2. Added a dynamic styling widget for the phone field
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Phone Number'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message (optional)', 'rows': 4}),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(str(i), f'{i} Star') for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'rating-radio'}),
        initial=5,
    )

    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Share your experience with us', 'rows': 4}),
        }


# 1. Add ContactMessage to your existing imports at the top:
# from .models import Booking, Review, ContactMessage

# 2. Add this class to the bottom of drivers/forms.py
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4}),
        }