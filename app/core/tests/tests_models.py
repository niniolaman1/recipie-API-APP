'''Test for models'''

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    '''Test models'''

    def test_create_user_with_email_successfull(self):
        '''Test creating user with email is successful'''
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test emailis normalized for new users.'''
        sample_emails = [
            ['test1@Example.com', 'test1@example.com'],
            ['test2@EXAMPLE.com', 'test2@example.com'],
            ['Test3@Example.com', 'Test3@example.com'],
            ['TEST4@EXAMPLE.COM', 'TEST4@example.com'],
            ['test5@example.COM', 'test5@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        '''Test that creating a user without an email raises a ValueError'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        '''Test creating a superuser.'''
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)