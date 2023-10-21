import os
from django.contrib.auth.password_validation import validate_password
from django.test import TestCase


class ConfigTest(TestCase):
    def test_secret_key_strenght(self):
        SECRET_KEY = os.environ.get('SECRET_KEY')
        try:
            validate_password(SECRET_KEY)
        except Exception as e:
            self.fail(f'Weak secret key - {e.messages}')
