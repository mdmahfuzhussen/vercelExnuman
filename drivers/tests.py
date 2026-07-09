from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Review


class ReviewFlowTests(TestCase):
    def test_booking_submission_sends_a_notification_email(self):
        user = User.objects.create_user(
            username='student',
            password='securepass123',
            first_name='Nadia',
            last_name='Rahman',
            email='student@example.com',
        )
        self.client.login(username='student', password='securepass123')

        with patch('drivers.views.send_mail') as mock_send_mail:
            response = self.client.post(reverse('drivers:booking'), {
                'name': 'Nadia Rahman',
                'email': 'student@example.com',
                'date': '2026-08-01',
                'time': '10:00',
                'message': 'Please confirm my test lesson.',
            })

        self.assertEqual(response.status_code, 302)
        mock_send_mail.assert_called_once()
        self.assertEqual(mock_send_mail.call_args.kwargs['recipient_list'], ['mdmahufuzmahi@gmail.com'])

    def test_logged_in_user_can_submit_review_and_it_is_shown(self):
        user = User.objects.create_user(
            username='student',
            password='securepass123',
            first_name='Nadia',
            last_name='Rahman',
        )
        self.client.login(username='student', password='securepass123')

        response = self.client.post(reverse('drivers:submit_review'), {
            'comment': 'Excellent lessons and clear guidance.',
            'rating': 5,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=user, comment='Excellent lessons and clear guidance.').exists())

        home_response = self.client.get(reverse('drivers:home'))
        self.assertContains(home_response, 'Excellent lessons and clear guidance.')
        self.assertContains(home_response, 'Nadia Rahman')
        self.assertContains(home_response, '5/5')

    def test_anonymous_user_must_login_to_submit_review(self):
        response = self.client.post(reverse('drivers:submit_review'), {
            'comment': 'This should not be saved.',
            'rating': 5,
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])
        self.assertFalse(Review.objects.filter(comment='This should not be saved.').exists())
