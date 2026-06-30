from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Event, RSVP


class RSVPAndDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='secret123')
        self.other_user = User.objects.create_user(username='bob', password='secret123')
        self.event = Event.objects.create(
            title='Tech Meetup',
            description='A useful meetup',
            location='Seattle',
            event_date=timezone.now().date(),
            event_time=timezone.now().time(),
            created_by=self.user,
        )
        self.other_event = Event.objects.create(
            title='Design Sprint',
            description='A creative workshop',
            location='Remote',
            event_date=timezone.now().date(),
            event_time=timezone.now().time(),
            created_by=self.other_user,
        )

    def test_toggle_rsvp_creates_and_removes_rsvp(self):
        self.client.login(username='alice', password='secret123')

        response = self.client.post(reverse('toggle_rsvp', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(RSVP.objects.filter(user=self.user, event=self.event).exists())

        response = self.client.post(reverse('toggle_rsvp', args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RSVP.objects.filter(user=self.user, event=self.event).exists())

    def test_home_page_filters_events_by_search_query(self):
        response = self.client.get(reverse('home'), {'q': 'tech'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tech Meetup')
        self.assertNotContains(response, 'Design Sprint')
