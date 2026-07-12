from django.db import models
from django.contrib.auth.models import User

COURSE_CHOICES = [
    ('Single Lesson - £40/hr', 'Single Lesson - £40/hr'),
    ('10 Lesson Package - £350', '10 Lesson Package - £350'),
    ('Test Preparation - £60/session', 'Test Preparation - £60/session'),
    ('1 Hour Offer - £34', '1 Hour Offer - £34'),
    ('2 Hour Intro Offer - £64', '2 Hour Intro Offer - £64'),
    ('2 Hour Assessment - £64', '2 Hour Assessment - £64'),
    ('6 Hour Offer - £198', '6 Hour Offer - £198'),
    ('10 Hour Block Booking - £330', '10 Hour Block Booking - £330'),
    ('20 Hour Course - £660', '20 Hour Course - £660'),
    ('30 Hour Course - £990', '30 Hour Course - £990'),
    ('10 Hour Rebook - £340', '10 Hour Rebook - £340'),
]

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, default='Single Lesson - £40/hr')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.date} {self.time}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def reviewer_name(self):
        return self.user.get_full_name() or self.user.username

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.rating}★"

# Add this to the bottom of drivers/models.py


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
