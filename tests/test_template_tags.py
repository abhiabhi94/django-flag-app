from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured

from flag.conf import settings
from flag.templatetags.flag_tags import get_app_name, get_model_name, has_flagged, render_flag_form, get_login_url
from tests.base import BaseTemplateTagsTest, FlagInstance


class TestFlagTemplateTest(BaseTemplateTagsTest):
    def test_get_model_name(self):
        self.assertEqual(get_model_name(self.post_1), 'Post')

    def test_get_app_name(self):
        self.assertEqual(get_app_name(self.post_1), 'post')

    def test_has_flagged_for_unauthenticated_user(self):
        user = self.MockUser()
        self.assertEqual(has_flagged(user, self.post_1), False)

    def test_has_flagged_for_authenticated_user(self):
        user = self.user_2
        post = self.post_1
        self.assertEqual(has_flagged(user, post), False)
        # flag the object
        self.set_flag(post, user)
        self.assertEqual(has_flagged(user, post), True)

    @patch.object(settings, 'LOGIN_URL', None)
    def test_login_url_without_setting_login_url(self):
        with self.assertRaises(ImproperlyConfigured) as error:
            get_login_url()
        self.assertIsInstance(error.exception, ImproperlyConfigured)

    @patch.object(settings, 'LOGIN_URL', '/login')
    def test_get_login_url_without_backward_slash(self):
        self.assertEqual(settings.LOGIN_URL + '/', get_login_url())

    @patch.object(settings, 'LOGIN_URL', '/login/')
    def test_login_url_with_backward_slash(self):
        self.assertEqual(get_login_url(), settings.LOGIN_URL)

    def test_render_flag_form(self):
        post = self.post_1
        user = self.user_2
        data = render_flag_form(post, user)

        self.assertEqual(data['app_name'], post._meta.app_label)
        self.assertEqual(data['model_name'], type(post).__name__)
        self.assertEqual(data['model_id'], post.id)
        self.assertEqual(data['user'], user)
        self.assertEqual(data['flag_reasons'], FlagInstance.reasons)
        self.assertEqual(data['has_flagged'], False)

        # flag the object
        self.set_flag(post, user)
        data = render_flag_form(post, user)

        self.assertEqual(data['app_name'], post._meta.app_label)
        self.assertEqual(data['model_name'], type(post).__name__)
        self.assertEqual(data['model_id'], post.id)
        self.assertEqual(data['user'], user)
        self.assertEqual(data['flag_reasons'], FlagInstance.reasons)
        self.assertEqual(data['has_flagged'], True)
