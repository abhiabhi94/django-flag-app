from django.contrib.admin import AdminSite

from flag.admin import FlaggedContentAdmin
from flag.models import Flag
from tests.base import BaseFlagTest


class FlagAdminTest(BaseFlagTest):
    @staticmethod
    def _mock_request(user):
        class MockRequest:
            pass

        request = MockRequest()
        request.user = user
        return request

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_admin = FlaggedContentAdmin(Flag, AdminSite())

    def setUp(self):
        super().setUp()
        self.request = self._mock_request(self.user_1)

    def test_link_to_content_object(self):
        post = self.post_1
        self.set_flag(model_obj=post)
        flag = Flag.objects.get_flag(post)

        self.assertEqual(self.model_admin.link_to_content_object.short_description, 'Edit object')
        self.assertEqual(
            self.model_admin.link_to_content_object(flag),
            f"<a href='/admin/post/post/{post.id}/change/'>Link</a>",
        )
