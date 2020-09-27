from rest_framework import status

from tests.base import BaseFlagAPITest, Flag, FlagInstance


class FlagAPIViewsTest(BaseFlagAPITest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.post = cls.create_post()

    def setUp(self):
        super().setUp()
        self.url = '/api/flag/'

    def test_flagging_successfully_with_url_encoded_form(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()['detail'],
            'The content has been flagged successfully. A moderator will review it shortly.'
        )

        # check database
        flag = Flag.objects.get_flag(post)
        __, created = FlagInstance.objects.get_or_create(
                flag=flag,
                user=response.wsgi_request.user,
                reason=data['reason']
                )
        self.assertEqual(created, False)

    def test_flagging_successfully_with_json_format(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()['detail'],
            'The content has been flagged successfully. A moderator will review it shortly.'
        )

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

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['detail'],
            [f'This content has already been flagged by the user ({self.user_1.username})']
        )

    def test_flagging_unflagged_object(self):
        post = self.post
        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['detail'],
            [f'This content has not been flagged by the user ({self.user_1.username})']
            )

    def test_unflagging_successfully(self):
        # un-flag => no reason is passed and the content must be already flagged by the user
        post = self.post
        self.set_flag(model_obj=post)
        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['detail'], 'The content has been unflagged successfully.')
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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_incorrect_reason(self):
        """Test response when incorrect reason is passed"""
        data = self.data.copy()
        reason = -1
        data['reason'] = reason
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], [f'{reason} is an invalid reason'])

    def test_choosing_last_reason_without_info(self):
        """Test response when incorrect reason is passed"""
        data = self.data.copy()
        reason = FlagInstance.reason_values[-1]
        data.update({'reason': reason})
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], ['Please supply some information as the reason for flagging'])

    def test_choosing_last_reason_with_info(self):
        """Test response when last reason is passed with info"""
        data = self.data.copy()
        post = self.post_2
        reason = FlagInstance.reason_values[-1]
        info = 'weird'
        data.update({'reason': reason, 'info': info, 'model_id': post.id})
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()['detail'],
            'The content has been flagged successfully. A moderator will review it shortly.'
        )
        # check database
        flag = Flag.objects.get_flag(post)
        self.assertEqual(FlagInstance.objects.get(user=response.wsgi_request.user, flag=flag).info, info)
