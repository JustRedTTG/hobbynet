from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test.testcases import TestCase, Client
from django.urls import reverse

from hobbynet.common.models import TITLE_MIN_LENGTH, NAME_MIN_LENGTH, NAME_MAX_LENGTH, TITLE_MAX_LENGTH
from hobbynet.common.tests import format_errors, model_blank_to_null
from hobbynet.profiles.views import TopicForm
from hobbynet.topics.models import Topic

UserModel = get_user_model()

VALID_TOPIC_DATA = {
    'title': 't' * TITLE_MIN_LENGTH,
    'visibility': '',
    'display_name': 't' * NAME_MIN_LENGTH,
}

INVALID_TOPIC_DATA = {
    'title': [
        '',  # blank display_name should be invalid
        't' * (TITLE_MAX_LENGTH + 1),  # too long display_name should be invalid
        't' * (TITLE_MIN_LENGTH - 1),  # too short display_name should be invalid
    ],
    'visibility': ['draft', 'spam'],
    'display_name': [
        't' * (NAME_MAX_LENGTH + 1),  # too long display_name should be invalid
        't' * (NAME_MIN_LENGTH - 1),  # too short display_name should be invalid
    ]
}


class TopicTestCase(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(email='red@redttg.com', password="a", display_name='a')
        self.client = Client()
        self.client.force_login(self.user)

    def topic_form_inject(self, kwargs):
        form = TopicForm(data=kwargs, initial={
            'user': self.user,
            'editor': self.user,
        })
        return form

    def topic_form_creation_valid(self, kwargs):
        form = self.topic_form_inject(kwargs)
        self.assertTrue(form.is_valid(), msg=f'Topic with {kwargs} should be valid\n{format_errors(form.errors)}')

    def topic_form_creation_invalid(self, kwargs, notice_key='key'):
        form = self.topic_form_inject(kwargs)
        self.assertFalse(form.is_valid(),
                         msg=f'Topic with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid\n{format_errors(form.errors)}')

    def topic_model_creation_valid(self, kwargs):
        kwargs = model_blank_to_null(kwargs)
        try:
            topic = self.user.topic_set.create(**kwargs)
        except IntegrityError as e:
            self.fail(f'Topic with {kwargs} should be valid, but got\nIntegrityError:\n{e}')
        except Exception as e:
            self.fail(f'Topic with {kwargs} should be valid, but got exception: {e}')
        self.assertIsNotNone(topic, msg=f'Topic with {kwargs} should be valid')

    def topic_model_creation_invalid(self, kwargs, notice_key='key'):
        kwargs = model_blank_to_null(kwargs)
        try:
            with transaction.atomic():
                self.user.topic_set.create(**kwargs)
            self.fail(f'Topic with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid')
        except IntegrityError:
            return
        except Exception as e:
            self.fail(f'Topic with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid, but got '
                      f'exception: {e}')

    def topic_view_creation_valid(self, kwargs):
        result = self.client.post(reverse('topic_create'), kwargs)
        self.assertEqual(result.status_code, 302, msg=f'Topic with {kwargs} should be valid')
        self.assertEqual(
            result.headers['Location'], reverse('profile_details_self'), msg=f'Topic with {kwargs} should be valid')

    def topic_view_creation_invalid(self, kwargs, notice_key='key'):
        result = self.client.post(reverse('register'), kwargs)
        self.assertEqual(result.status_code, 200,
                         msg=f'Topic with {notice_key}="{kwargs.get(notice_key, "___")}" should be invalid')

    def test_topic_model_creation_with_valid_data(self):
        self.topic_model_creation_valid(VALID_TOPIC_DATA)

    def test_topic_model_creation_with_invalid_data(self):
        for key, values in INVALID_TOPIC_DATA.items():
            for value in values:
                if value != '':
                    continue
                kwargs = VALID_TOPIC_DATA.copy()
                kwargs[key] = value
                self.topic_model_creation_invalid(kwargs, key)

    def test_topic_form_creation_with_valid_data(self):
        self.topic_form_creation_valid(VALID_TOPIC_DATA)

    def test_topic_form_creation_with_invalid_data(self):
        for key, values in INVALID_TOPIC_DATA.items():
            for value in values:
                kwargs = VALID_TOPIC_DATA.copy()
                kwargs[key] = value
                self.topic_form_creation_invalid(kwargs, key)

    def test_topic_view_creation_with_valid_data(self):
        self.topic_view_creation_valid(VALID_TOPIC_DATA)

    def test_topic_view_creation_with_invalid_data(self):
        for key, values in INVALID_TOPIC_DATA.items():
            for value in values:
                kwargs = VALID_TOPIC_DATA.copy()
                kwargs[key] = value
                self.topic_view_creation_invalid(kwargs, key)
