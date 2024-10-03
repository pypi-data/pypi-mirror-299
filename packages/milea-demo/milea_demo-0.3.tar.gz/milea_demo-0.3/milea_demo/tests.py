from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from milea_notify.models import Notification

from .models import DefaultModal, Tag


class DefaultModalTests(TestCase):

    def setUp(self):
        # Erstellen eines Benutzers für das Manager-Feld
        self.user = get_user_model().objects.create_user(email='test@user.com', password='12345', is_staff=True)

        # Erstellen eines Tags für das ManyToMany-Feld
        self.tag = Tag.objects.create(tag_name='TestTag')

    def test_default_modal_creation(self):
        default_modal = DefaultModal.objects.create(
            name='Test Name',
            email='test@example.com',
            url='http://www.example.com',
            text='This is a test text.',
            decimal=9.99,
            date=timezone.now().date(),
            time=timezone.now().time(),
            timestamp=timezone.now(),
            radio='choice1',
            manager=self.user,
        )
        default_modal.tags.add(self.tag)
        default_modal.save()

        self.assertEqual(DefaultModal.objects.count(), 1)
        self.assertEqual(default_modal.name, 'Test Name')
        self.assertIn(self.tag, default_modal.tags.all())
        self.assertTrue(default_modal.boolean is False)
        self.assertEqual(default_modal.manager.email, 'test@user.com')


class SignalTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@user.com', password='12345', is_staff=True)

    def test_create_manager_notification(self):
        DefaultModal.objects.create(
            name='Signal Test',
            email='signaltest@example.com',
            date=timezone.now().date(),
            time=timezone.now().time(),
            timestamp=timezone.now(),
            manager=self.user,
        )

        # Überprüfen, ob eine Benachrichtigung erstellt wurde
        notification_count = Notification.objects.filter(user=self.user).count()
        self.assertEqual(notification_count, 1)

        # Überprüfen Sie weitere Eigenschaften der Benachrichtigung, z.B. Titel und Inhalt
        notification = Notification.objects.get(user=self.user)
        self.assertEqual(notification.title, "Neues Demo Object")
        self.assertIn("Demo Benachrichtigung", notification.content)

class ProfileSettingTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='test@user.com', password='12345', is_staff=True)

    def test_user_option(self):

        option = self.user.profile.get_option('milea_demo', 'AppUserOption', 'can_view_others')
        self.assertEqual(option, True)
