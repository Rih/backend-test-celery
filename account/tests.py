# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# Standard libs
from unittest.mock import patch
from captcha.client import RecaptchaResponse
from django.contrib.auth.models import User
from django.test import TestCase, override_settings, tag
from django.urls import reverse

from .factories import EmailTokenFactory, UserFactory
from .models import EmailToken


@override_settings(
    MEDIA_ROOT='/app/test_media/',
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
)
class AccountTest(TestCase):

    fixtures = [
        'site'
    ]

    def setUp(self):
        self.user = UserFactory(username='john', email='test@account.cl')
        self.user.set_password('pass')
        self.user.save()
        self.client.login(username='john', password='pass')

    @tag('get_sign_up')
    def test_get_sign_up(self):
        # python manage.py test --tag=get_sign_up
        response = self.client.get(reverse('account:sign_up'))
        self.assertEqual(response.status_code, 200)

    @tag('post_sign_up')
    @patch("captcha.fields.client.submit")
    def test_post_sign_up(self, mocked_submit):
        # python manage.py test --tag=post_sign_up
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(
            reverse('account:sign_up'),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@doe.com',
                'password': 'doe1234',
                'g-recaptcha-response': 'PASSED'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        user = User.objects.latest('date_joined')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@doe.com')
        self.assertFalse(user.emailtoken.verified)
        self.assertTrue(user.emailtoken.token != '')

        # test email repeated
        response = self.client.post(
            reverse('account:sign_up'),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@doe.com',
                'password': 'doe1234',
                'g-recaptcha-response': 'PASSED'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email already registered')

    @tag('get_login')
    def test_get_login(self):
        # python manage.py test --tag=get_login
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, 302)

    @tag('redirect_logged_in')
    def test_redirect_logged_in(self):
        # Create a user
        # python manage.py test --tag=redirect_logged_in
        user = UserFactory(
            username="pepe",
            email='pepe@testing.cl',
        )
        user.set_password('1234567')
        user.save()
        # Login user
        self.client.login(username='lucho', password='1234567')
        resp = self.client.get(reverse('account:login'))

        # Check our user is logged in
        self.assertEqual(resp.status_code, 302)

        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)

    @tag('logout')
    def test_logout(self):
        # python manage.py test --tag=logout
        response = self.client.get(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)

    @tag('post_login')
    @patch("captcha.fields.client.submit")
    def test_post_login(self, mocked_submit):
        # python manage.py test --tag=post_login
        self.client.logout()
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        user = UserFactory(email='john@doe.com', username='someuser')
        user.set_password('pass')
        user.save()
        response = self.client.post(
            reverse('account:login'),
            {
                'email': 'john@doe.com',
                'password': 'pass',
                'g-recaptcha-response': 'PASSED'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

    @tag('post_login_wrong_pass')
    @patch("captcha.fields.client.submit")
    def test_post_login_wrong_pass(self, mocked_submit):
        # python manage.py test --tag=post_login_wrong_pass
        self.client.logout()
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        user = UserFactory(email='john@doe.com', username='someuser')
        user.set_password('pass')
        user.save()
        response = self.client.post(
            reverse('account:login'),
            {
                'email': 'john@doe.com',
                'password': 'doe1234',
                'g-recaptcha-response': 'PASSED'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')
        # email doesnot exists
        response = self.client.post(
            reverse('account:login'),
            {
                'email': 'john@doe.not',
                'password': 'doe1234',
                'g-recaptcha-response': 'PASSED'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')

    @tag('get_email_confirmation')
    def test_get_email_confirmation(self):
        # python manage.py test --tag=get_email_confirmation
        EmailTokenFactory(token='a1wqeq2aasd')
        response = self.client.get(
            reverse('account:verify_email', kwargs={'token': 'a1wqeq2aasd'})
        )
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Your email has been confirmed already')
        token = EmailToken.objects.get(token='a1wqeq2aasd')
        self.assertTrue(token.verified)

    @tag('get_email_confirmation_not_found')
    def test_get_email_confirmation_not_found(self):
        # python manage.py test --tag=get_email_confirmation_not_found
        self.test_get_email_confirmation()
        response = self.client.get(
            reverse('account:verify_email', kwargs={'token': 'a1wqeq2aasdas'})
        )
        self.assertEquals(response.status_code, 404)

    @tag('post_email_unverified')
    def test_post_email_unverified(self):
        # python manage.py test --tag=post_email_unverified
        self.test_post_sign_up()
        response = self.client.post(reverse('account:email_unverified'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'We sent you a confirmation link')
