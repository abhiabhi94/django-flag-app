from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import reverse
from django.test import Client, RequestFactory, TestCase
from rest_framework.test import APITestCase

from flag.models import Flag, FlagInstance
from testapp.post.models import Post


User = get_user_model()


class BaseFlagTestUtils:
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_1 = User.objects.create_user(
                    username='test-1',
                    email='a@a.com',
                    password='1234'
        )
        cls.user_2 = User.objects.create_user(
            username='test-2',
            email='b@b.com',
            password='1234'
        )
        cls.moderator = User.objects.create_user(
            username='moderator',
            email='b@b.com',
            password='1234'
        )
        moderator_group = Group.objects.filter(name='flag_moderator').first()
        moderator_group.user_set.add(cls.moderator)
        cls.posts = 0
        cls.post_1 = cls.create_post()
        cls.post_2 = cls.create_post()
        content_type = ContentType.objects.get(model=type(cls.post_1).__name__.lower())
        cls.content_object_1 = content_type.get_object_for_this_type(id=cls.post_1.id)
        cls.content_object_2 = content_type.get_object_for_this_type(id=cls.post_2.id)
        cls.flags = 0

    def setUp(self):
        super().setUp()
        self.client.force_login(self.user_1)
        self.url = reverse('flag:flag')
        self.data = {
            'app_name': 'post',
            'model_name': 'Post',
            'model_id': self.post_1.id,
            'reason': FlagInstance.reason_values[0],
            'info': ''
        }
        self.addCleanup(patch.stopall)

    @classmethod
    def create_post(cls):
        cls.posts += 1
        return Post.objects.create(
            user=cls.user_1,
            title=f'post {cls.posts}',
            body=f'post number {cls.posts} body'
        )

    @classmethod
    def increase_flag_count(cls):
        cls.flags = 1

    @classmethod
    def create_flag(cls, ct_object=None, creator=None):
        if not ct_object:
            ct_object = cls.content_object_1
        if not creator:
            creator = cls.user_1
        return Flag.objects.create(content_object=ct_object, creator=creator)

    @classmethod
    def set_flag(cls, model_obj=None, user=None, reason=None, info=None):
        if not user:
            user = cls.user_1
        if not reason:
            reason = FlagInstance.reason_values[0]
        if not info:
            info = None
        if not model_obj:
            model_obj = cls.post_1
        flag_obj = Flag.objects.get_flag(model_obj)
        cls.increase_flag_count()
        return FlagInstance.objects.create(
            flag=flag_obj,
            user=user,
            reason=reason,
            info=info
        )


class BaseFlagTest(BaseFlagTestUtils, TestCase):
    pass


class BaseFlagModelTest(BaseFlagTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.flag = cls.create_flag()


class BaseFlagViewTest(BaseFlagTest):
    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.force_login(self.user_1)

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.flag_instance = cls.set_flag()


class BaseTemplateTagsTest(BaseFlagTest):
    class MockUser:
        """Mock unauthenticated user for template. The User instance always returns True for `is_authenticated`"""
        is_authenticated = False

    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()


class BaseFlagMixinsTest(BaseFlagTest):
    def setUp(self):
        super().setUp()
        self.data = {
            'app_name': 'post',
            'model_name': 'Post',
            'model_id': self.post_1.id
        }
        self.factory = RequestFactory()


class BaseFlagAPITest(BaseFlagTestUtils, APITestCase):
    pass
