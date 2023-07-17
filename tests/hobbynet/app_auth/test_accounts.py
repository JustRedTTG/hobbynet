from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test.testcases import TestCase, Client
from django.urls import reverse

from hobbynet.app_auth.forms import RegisterAccountForm
from hobbynet.common.models import NAME_MAX_LENGTH, NAME_MIN_LENGTH

UserModel = get_user_model()

VALID_ACCOUNT_DATA = {
    'email': 'red@redttg.com',
    'password': '"[(red123!@#$%абв^&*)]//"\\-+,.|_=~`',
}

VALID_PROFILE_DATA = {
    'email': VALID_ACCOUNT_DATA['email'],
    'password1': VALID_ACCOUNT_DATA['password'],
    'password2': VALID_ACCOUNT_DATA['password'],
    'display_name': 't' * NAME_MIN_LENGTH,
}

INVALID_ACCOUNT_DATA = {
    'email': [
        '',  # blank email should be invalid
        'red', 'red@',
        '@redttg.com', 'red@redttg', 'red space@redttg.com', 'red space@redttg',
        'red.com', 'red@.com', 'red@redttg.', '$@redttg.com', '^@redttg.com',
        'red@^redttg.com', 'red@redttg^com', 'red@redttg.^',
        'red@$redttg.com', 'red@redttg$com', 'red@redttg.$'
    ],
    'password': [
        ''  # blank password should be invalid
    ]
}

INVALID_PROFILE_DATA = {
    'email': INVALID_ACCOUNT_DATA['email'],
    'password1': INVALID_ACCOUNT_DATA['password'],
    'password2': INVALID_ACCOUNT_DATA['password'],
    'display_name': [
        '',  # blank display_name should be invalid
        't' * (NAME_MAX_LENGTH + 1),  # too long display_name should be invalid
        't' * (NAME_MIN_LENGTH - 1),  # too short display_name should be invalid
    ]
}


class AccountTestCase(TestCase):
    def account_model_creation_valid(self, kwargs):
        try:
            user = UserModel.objects.create_user(**kwargs)
        except (ValueError, ValidationError):
            self.fail(f'Account with {kwargs} should be valid')
        except Exception as e:
            self.fail(f'Account with {kwargs} should be valid, but got exception: {e}')
        self.assertIsNotNone(user, msg=f'Account with {kwargs} should be valid')

    def account_form_creation_valid(self, kwargs):
        form = RegisterAccountForm(data=kwargs)
        self.assertTrue(form.is_valid(), msg=f'Account with {kwargs} should be valid')

    def account_form_creation_invalid(self, kwargs, notice_key='key'):
        form = RegisterAccountForm(data=kwargs)
        self.assertFalse(form.is_valid(),
                         msg=f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid')

    def account_model_creation_invalid(self, kwargs, notice_key='key'):
        with self.assertRaises((ValueError, ValidationError),
                               msg=f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid'):
            UserModel.objects.create_user(**kwargs)

    def account_view_creation_valid(self, kwargs):
        result = Client().post(reverse('register'), kwargs)
        self.assertEqual(result.status_code, 302, msg=f'Account with {kwargs} should be valid')
        self.assertEqual(
            result.headers['Location'], reverse('profile_details_self'), msg=f'Account with {kwargs} should be valid')

    def account_view_creation_invalid(self, kwargs, notice_key='key'):
        result = Client().post(reverse('register'), kwargs)
        self.assertEqual(result.status_code, 200,
                         msg=f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid')

    def test_account_model_creation_with_valid_data(self):
        self.account_model_creation_valid(VALID_ACCOUNT_DATA)

    def test_account_model_creation_with_invalid_data(self):
        for key, values in INVALID_ACCOUNT_DATA.items():
            for value in values:
                kwargs = VALID_ACCOUNT_DATA.copy()
                kwargs[key] = value
                self.account_model_creation_invalid(kwargs, key)

    def test_account_form_creation_with_valid_data(self):
        self.account_form_creation_valid(VALID_PROFILE_DATA)

    def test_account_form_creation_with_invalid_data(self):
        for key, values in INVALID_PROFILE_DATA.items():
            for value in values:
                kwargs = VALID_PROFILE_DATA.copy()
                kwargs[key] = value
                self.account_form_creation_invalid(kwargs, key)

    def test_account_view_creation_with_valid_data(self):
        self.account_view_creation_valid(VALID_PROFILE_DATA)

    def test_account_view_creation_with_invalid_data(self):
        for key, values in INVALID_PROFILE_DATA.items():
            for value in values:
                kwargs = VALID_PROFILE_DATA.copy()
                kwargs[key] = value
                self.account_view_creation_invalid(kwargs, key)
