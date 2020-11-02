from flag.conf import settings
from tests.base import BaseFlagViewTest, Client, Flag, FlagInstance


class TestSetFlag(BaseFlagViewTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.post = cls.create_post()

    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.force_login(self.user_1)

    def test_flagging_successfully(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 0,
            'flag': 1,
            'msg': 'The content has been flagged successfully. A moderator will review it shortly.'
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

        # check database
        flag = Flag.objects.get_flag(post)
        __, created = FlagInstance.objects.get_or_create(
                flag=flag,
                user=response.wsgi_request.user,
                reason=data['reason']
                )
        self.assertEqual(created, False)

    def test_flagging_flagged_object(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        self.set_flag(post)
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 1,
            'msg': [f'This content has already been flagged by the user ({self.user_1.username})']
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

    def test_flagging_unflagged_object(self):
        post = self.post
        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 1,
            'msg': [f'This content has not been flagged by the user ({self.user_1.username})']
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

    def test_unflagging_successfully(self):
        # un-flag => no reason is passed and the content must be already flagged by the user
        post = self.post
        self.set_flag(model_obj=post)
        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 0,
            'msg': 'The content has been unflagged successfully.'
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)
        # check database
        flag = Flag.objects.get_flag(post)
        __, created = FlagInstance.objects.get_or_create(
                flag=flag,
                user=response.wsgi_request.user,
                reason=FlagInstance.reason_values[0]
                )
        self.assertEqual(created, True)

    def test_set_flag_for_unauthenticated_user(self):
        """Test whether unauthenticated user can create/delete flag using view"""
        self.client.logout()
        url = self.url
        response = self.client.post(url, data=self.data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '{}?next={}'.format(settings.LOGIN_URL, url))

    def test_incorrect_reason(self):
        """Test response when incorrect reason is passed"""
        data = self.data.copy()
        reason = -1
        data['reason'] = reason
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 1,
            'msg': [f'{reason} is an invalid reason']
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)

    def test_choosing_last_reason_without_info(self):
        """Test response when incorrect reason is passed"""
        data = self.data.copy()
        reason = FlagInstance.reason_values[-1]
        data.update({'reason': reason})
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 1,
            'msg': ['Please supply some information as the reason for flagging']
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), response_data)

    def test_choosing_last_reason_with_info(self):
        """Test response when last reason is passed with info"""
        data = self.data.copy()
        post = self.post_2
        reason = FlagInstance.reason_values[-1]
        info = 'weird'
        data.update({'reason': reason, 'info': info, 'model_id': post.id})
        response = self.client.post(self.url, data=data)
        response_data = {
            'status': 0,
            'flag': 1,
            'msg': 'The content has been flagged successfully. A moderator will review it shortly.'
        }
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), response_data)
        # check database
        flag = Flag.objects.get_flag(post)
        self.assertEqual(FlagInstance.objects.get(user=response.wsgi_request.user, flag=flag).info, info)
