from rest_framework import status

from flag.api.serializers import FlagSerializer
from tests.base import BaseFlagAPITest, Flag, FlagInstance


class FlagAPIViewsTest(BaseFlagAPITest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.post = cls.create_post()
        cls.flag = Flag.objects.get_flag(cls.post)

    def setUp(self):
        super().setUp()
        self.url = '/api/flag/'
        self.init_count = 0
        self.context = {
            'model_obj': self.post,
            'user': self.user_1
        }

    def test_flagging_successfully_with_url_encoded_form(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        self.flag.refresh_from_db()
        init_count = self.flag.count

        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flag.refresh_from_db()
        self.assertEqual(response.data, FlagSerializer(self.flag, context=self.context).data)

        # check database
        __, created = FlagInstance.objects.get_or_create(
                flag=self.flag,
                user=response.wsgi_request.user,
                reason=data['reason']
                )
        self.assertEqual(created, False)
        self.assertEqual(self.flag.count, init_count + 1)

    def test_flagging_successfully_with_json_format(self):
        data = self.data.copy()
        post = self.post
        data['model_id'] = post.id
        response = self.client.post(self.url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flag.refresh_from_db()
        self.assertEqual(response.data, FlagSerializer(self.flag, context=self.context).data)

        # check database
        __, created = FlagInstance.objects.get_or_create(
                flag=self.flag,
                user=response.wsgi_request.user,
                reason=data['reason']
                )
        self.assertEqual(created, False)
        self.assertEqual(self.flag.count, self.init_count + 1)

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
        self.flag.refresh_from_db()
        init_count = self.flag.count
        self.set_flag(post)
        self.flag.refresh_from_db()
        self.assertEqual(self.flag.count, init_count + 1)

        data = self.data.copy()
        data['model_id'] = post.id
        data.pop('reason')
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.flag.refresh_from_db()
        self.assertEqual(response.data, FlagSerializer(self.flag, context=self.context).data)
        # check database
        self.assertEqual(self.flag.count, init_count)
        __, created = FlagInstance.objects.get_or_create(
                flag=self.flag,
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
        flag = Flag.objects.get_flag(post)
        init_count = flag.count
        reason = FlagInstance.reason_values[-1]
        info = 'weird'
        data.update({'reason': reason, 'info': info, 'model_id': post.id})
        response = self.client.post(self.url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        flag.refresh_from_db()
        context = self.context.copy()
        context['model_obj'] = post
        self.assertEqual(response.data, FlagSerializer(flag, context=context).data)
        # check database
        self.assertEqual(FlagInstance.objects.get(user=response.wsgi_request.user, flag=flag).info, info)
        self.assertEqual(flag.count, init_count + 1)
