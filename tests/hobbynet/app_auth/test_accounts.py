from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test.testcases import TestCase, Client
from django.urls import reverse

from hobbynet.app_auth.forms import RegisterAccountForm
from hobbynet.common.models import NAME_MAX_LENGTH, NAME_MIN_LENGTH
from hobbynet.common.tests import format_errors, model_blank_to_null
from hobbynet.profiles.models import Profile

UserModel = get_user_model()

VALID_ACCOUNT_DATA = {
    'email': 'red@redttg.com',
    'password': '"[(red123!@#$%абв^&*)]//"\\-+,.|_=~`',
    'display_name': 't' * NAME_MIN_LENGTH,
}

VALID_PROFILE_DATA = {
    'email': VALID_ACCOUNT_DATA['email'],
    'password1': VALID_ACCOUNT_DATA['password'],
    'password2': VALID_ACCOUNT_DATA['password'],
    'display_name': VALID_ACCOUNT_DATA['display_name'],
}

INVALID_ACCOUNT_DATA = {
    'email': [
        '',  # blank email should be invalid
        'red', 'red@',
        '@redttg.com', 'red@redttg', 'red space@redttg.com', 'red space@redttg',
        'red.com', 'red@.com', 'red@redttg.', '$@redttg.com', '^@redttg.com',
        'red@^redttg.com', 'red@redttg^com', 'red@redttg.^',
        'red@$redttg.com', 'red@redttg$com', 'red@redttg.$'
    ]
}

INVALID_PROFILE_DATA = {
    'email': INVALID_ACCOUNT_DATA['email'],
    'password1': [
        ''  # blank password should be invalid
    ],
    'display_name': [
        '',  # blank display_name should be invalid
        't' * (NAME_MAX_LENGTH + 1),  # too long display_name should be invalid
        't' * (NAME_MIN_LENGTH - 1),  # too short display_name should be invalid
    ]
}
INVALID_PROFILE_DATA['password2'] = INVALID_PROFILE_DATA['password1']


class AccountTestCase(TestCase):
    def account_form_creation_valid(self, kwargs):
        form = RegisterAccountForm(data=kwargs)
        self.assertTrue(form.is_valid(), msg=f'Account with {kwargs} should be valid\n{format_errors(form.errors)}')
        try:
            return form.save()
        except ValueError:
            pass
        except Exception as e:
            self.fail(f'Account with {kwargs} should be valid, but got exception: {e}')

    def account_form_creation_invalid(self, kwargs, notice_key='key'):
        form = RegisterAccountForm(data=kwargs)
        self.assertFalse(form.is_valid(),
                         msg=f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid\n'
                             f'{format_errors(form.errors)}')

    def account_model_creation_valid(self, kwargs):
        kwargs = model_blank_to_null(kwargs)
        try:
            with transaction.atomic():
                user = UserModel.objects.create_user(**kwargs)
        except IntegrityError as e:
            self.fail(f'Account with {kwargs} should be valid, but got\nIntegrityError:\n{e}')
        except Exception as e:
            self.fail(f'Account with {kwargs} should be valid, but got exception: {e}')
        self.assertIsNotNone(user, msg=f'Account with {kwargs} should be valid')
        return user

    def account_model_creation_invalid(self, kwargs, notice_key='key'):
        kwargs = model_blank_to_null(kwargs)
        try:
            with transaction.atomic():
                UserModel.objects.create_user(**kwargs)
            self.fail(f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid')
        except IntegrityError:
            return
        except Exception as e:
            self.fail(f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid, but got '
                      f'exception: {e}')

    def account_view_creation_valid(self, kwargs):
        result = Client().post(reverse('register'), kwargs)
        self.assertEqual(result.status_code, 302, msg=f'Account with {kwargs} should be valid')
        self.assertEqual(
            result.headers['Location'], reverse('profile_details_self'), msg=f'Account with {kwargs} should be valid')
        if result.status_code == 302:
            return UserModel.objects.last()

    def account_view_creation_invalid(self, kwargs, notice_key='key'):
        result = Client().post(reverse('register'), kwargs)
        self.assertEqual(result.status_code, 200,
                         msg=f'Account with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid')

    def test_account_model_creation_with_valid_data(self):
        user = self.account_model_creation_valid(VALID_ACCOUNT_DATA)
        self.user_profiles_check(user)

    def test_account_model_creation_with_invalid_data(self):
        for key, values in INVALID_ACCOUNT_DATA.items():
            for value in values:
                if value != '':
                    continue
                kwargs = VALID_ACCOUNT_DATA.copy()
                kwargs[key] = value
                self.account_model_creation_invalid(kwargs, key)

    def test_account_form_creation_with_valid_data(self):
        user = self.account_form_creation_valid(VALID_PROFILE_DATA)
        self.user_profiles_check(user)

    def test_account_form_creation_with_invalid_data(self):
        for key, values in INVALID_PROFILE_DATA.items():
            for value in values:
                kwargs = VALID_PROFILE_DATA.copy()
                kwargs[key] = value
                self.account_form_creation_invalid(kwargs, key)

    def test_account_view_creation_with_valid_data(self):
        user = self.account_view_creation_valid(VALID_PROFILE_DATA)
        self.user_profiles_check(user)

    def test_account_view_creation_with_invalid_data(self):
        for key, values in INVALID_PROFILE_DATA.items():
            for value in values:
                kwargs = VALID_PROFILE_DATA.copy()
                kwargs[key] = value
                self.account_view_creation_invalid(kwargs, key)

    def user_profiles_check(self, user):
        # Check if user is valid
        self.assertIsNotNone(user, msg=f'Valid user should not be None, '
                                       f'did the test fail?')
        self.assertIsInstance(user, UserModel, msg=f'Valid user should be instance of '
                                                   f'UserModel')
        # Refresh user from database to simulate a fresh User object
        user = UserModel.objects.get(pk=user.pk)
        # Check if user is in the database
        self.assertIsNotNone(user, msg=f'Valid user should be in the database')
        profile = Profile.objects.get(user=user)
        # Check if user has a profile
        self.assertIsNotNone(profile, msg=f'Valid user should have a profile')
        # Check if profile is valid
        self.assertEqual(user.profile.display_name, VALID_PROFILE_DATA['display_name'],
                         msg=f'Valid user should have display_name='
                             f'"{VALID_PROFILE_DATA["display_name"]}')
        profile_pk = user.profile.pk
        user.delete()
        # Check if the profile is deleted with the user
        self.assertIsNone(Profile.objects.filter(pk=profile_pk).first(), msg=f'Profile {profile_pk} should be '
                                                                             f'deleted with user')
