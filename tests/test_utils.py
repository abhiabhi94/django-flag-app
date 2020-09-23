from unittest.mock import patch

from django.contrib.contenttypes.models import ContentType

from flag.utils import get_content_type, get_model_object, process_flagging_request, get_user_for_model
from tests.base import BaseFlagTest, Post


class TestGetContentType(BaseFlagTest):
    def test_success(self):
        post = self.post_1
        response = get_content_type(post)
        self.assertEqual(response, ContentType.objects.get_for_model(post.__class__))


class TestGetModelObject(BaseFlagTest):
    def test_success(self):
        data = self.data.copy()
        data.pop('info')
        data.pop('reason')
        response = get_model_object(**data)
        post = Post.objects.get(id=data['model_id'])
        self.assertEqual(response, post)


class TestGetUserForModel(BaseFlagTest):
    def test_when_user_field_is_associated(self):
        response = get_user_for_model(self.post_1)
        self.assertEqual(response, self.post_1.user)

    @patch('testapp.post.models.Post')
    def test_when_user_field_is_not_associated(self, mocked_post_model):
        mocked_post = mocked_post_model()
        response = get_user_for_model(mocked_post)
        self.assertEqual(response, None)


class TestProcessFlaggingRequest(BaseFlagTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.post = cls.create_post()

    def test_flagging_successfully(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        response = process_flagging_request(user=self.user_1, model_obj=post, data=data)
        response_data = {
            'status': 0,
            'flag': 1,
            'msg': 'The content has been flagged successfully. A moderator will review it shortly.'
        }
        self.assertDictEqual(response, response_data)

    def test_unflagging_successfully(self):
        post = self.post
        self.set_flag(model_obj=post)
        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = process_flagging_request(user=self.user_1, model_obj=post, data=data)
        response_data = {
            'status': 0,
            'msg': 'The content has been unflagged successfully.'
        }

        self.assertDictEqual(response, response_data)

    def test_flagging_flagged_object(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        self.set_flag(post)
        response = process_flagging_request(user=self.user_1, model_obj=self.post, data=data)
        response_data = {
            'status': 1,
            'msg': [f'This content has already been flagged by the user ({self.user_1.username})']
        }
        self.assertDictEqual(response, response_data)

    def test_flagging_unflagged_object(self):
        post = self.post
        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = process_flagging_request(user=self.user_1, model_obj=self.post, data=data)
        response_data = {
            'status': 1,
            'msg': [f'This content has not been flagged by the user ({self.user_1.username})']
        }
        self.assertDictEqual(response, response_data)
