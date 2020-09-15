from flag.templatetags.flag_tags import get_app_name, get_model_name, has_flagged, render_flag_form
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

    def test_render_flag_form(self):
        post = self.post_1
        user = self.user_2
        data = render_flag_form(post, user)

        self.assertEqual(data['app_name'], post._meta.app_label)
        self.assertEqual(data['model_name'], type(post).__name__)
        self.assertEqual(data['model_id'], post.id)
        self.assertEqual(data['flag_reasons'], FlagInstance.reasons)
        self.assertEqual(data['has_flagged'], False)

        # flag the object
        self.set_flag(post, user)
        data = render_flag_form(post, user)

        self.assertEqual(data['app_name'], post._meta.app_label)
        self.assertEqual(data['model_name'], type(post).__name__)
        self.assertEqual(data['model_id'], post.id)
        self.assertEqual(data['flag_reasons'], FlagInstance.reasons)
        self.assertEqual(data['has_flagged'], True)
