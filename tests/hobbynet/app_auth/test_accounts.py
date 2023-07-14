from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test.testcases import TestCase, Client
from django.urls import reverse

UserModel = get_user_model()

VALID_ACCOUNT_DATA = {
    'email': 'red@redttg.com',
    'password': '"[(red123!@#$%абв^&*)]//"\\-+,.|_=~`',
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


class AccountTestCase(TestCase):
    def account_model_creation_valid(self, kwargs):
        try:
            user = UserModel.objects.create_user(**kwargs)
        except (ValueError, ValidationError):
            self.fail(f'Account with {kwargs} should be valid')
        except Exception as e:
            self.fail(f'Account with {kwargs} should be valid, but got exception: {e}')
        self.assertIsNotNone(user)

    def account_form_creation_valid(self, kwargs):



    def account_model_creation_invalid(self, kwargs, notice_key='key'):
        with self.assertRaises((ValueError, ValidationError),
                               msg=f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid'):
            UserModel.objects.create_user(**kwargs)


    def test_account_model_creation_with_valid_data(self):
        self.account_model_creation_valid(VALID_ACCOUNT_DATA)

    def test_account_model_creation_with_invalid_data(self):
        for key, values in INVALID_ACCOUNT_DATA.items():
            for value in values:
                kwargs = VALID_ACCOUNT_DATA.copy()
                kwargs[key] = value
                self.account_model_creation_invalid(kwargs, key)

    def test_account_form_creation_with_valid_data(self):
        self.account_form_creation_valid(VALID_ACCOUNT_DATA)

    def test_account_form_creation_with_invalid_data(self):
        for key, values in INVALID_ACCOUNT_DATA.items():
            for value in values:
                kwargs = VALID_ACCOUNT_DATA.copy()
                kwargs[key] = value
                self.account_form_creation_invalid(kwargs, key)

