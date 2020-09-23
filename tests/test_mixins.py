from django.views import View
from django.http.response import JsonResponse
from rest_framework.views import APIView

from tests.base import BaseFlagMixinsTest, Post
from flag.mixins import AJAXMixin, ContentTypeMixin


class MockedAJAXView(AJAXMixin, View):
    pass


class MockedContentTypeView(ContentTypeMixin, View):
    api = False

    def post(self, request, *args, **kwargs):
        return JsonResponse({})


class MockedContentTypeAPIView(ContentTypeMixin, APIView):
    api = True

    def post(self, request, *args, **kwargs):
        self.validate(request)
        return JsonResponse({})


class TestAJAXMixin(BaseFlagMixinsTest):
    def setUp(self):
        super().setUp()
        self.view = MockedAJAXView()

    def test_non_ajax_response_post_required(self):
        request = self.factory.post(self.url)
        response = self.view.dispatch(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'Only AJAX requests are allowed')


class TestContentTypeMixin(BaseFlagMixinsTest):
    def setUp(self):
        super().setUp()
        self.view = MockedContentTypeView()

    def get_response(self, data):
        request = self.factory.post(self.url, data=data)
        return self.view.dispatch(request)

    def test_without_any_data(self):
        request = self.factory.post(self.url)
        response = self.view.dispatch(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'no data passed')

    def test_without_app_name(self):
        data = self.data.copy()
        data.pop('app_name')
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'app name is required')

    def test_without_model_name(self):
        data = self.data.copy()
        data.pop('model_name')
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'model name is required')

    def test_without_model_id(self):
        data = self.data.copy()
        data.pop('model_id')
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'model id is required')

    def test_invalid_app_name(self):
        data = self.data.copy()
        val = 'not exists'
        data['app_name'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, f'{val} is not a valid app name')

    def test_invalid_model_name(self):
        data = self.data.copy()
        val = 'not exists'
        data['model_name'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, f'"{val}" is NOT a valid model name')

    def test_model_id_which_doesnt_exist(self):
        data = self.data.copy()
        val = 100
        data['model_id'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            self.view.error,
            f'"{val}" is NOT a valid model id for the model "{data["model_name"]}"')

    def test_non_integral_model_id(self):
        data = self.data.copy()
        val = 'c'
        data['model_id'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            self.view.error,
            f'model id must be an integer, "{val}" is NOT')

    def test_success(self):
        data = self.data.copy()
        data['model_id'] = str(data['model_id'])
        response = self.get_response(data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.view.error)
        self.assertEqual(self.view.data, data)
        self.assertEqual(self.view.model_name, data['model_name'])
        self.assertEqual(self.view.app_name, data['app_name'])
        self.assertEqual(self.view.model_id, int(data['model_id']))
        self.assertEqual(self.view.model_obj, Post.objects.get(id=data['model_id']))


class TestContentTypeMixinForAPI(BaseFlagMixinsTest):
    def setUp(self):
        super().setUp()
        self.view = MockedContentTypeAPIView()

    def get_response(self, data):
        request = self.factory.post(self.url, data=data)
        return self.view.dispatch(request)

    def test_without_any_data(self):
        request = self.factory.post(self.url)
        response = self.view.dispatch(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'no data passed')

    def test_without_app_name(self):
        data = self.data.copy()
        data.pop('app_name')
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'app name is required')

    def test_without_model_name(self):
        data = self.data.copy()
        data.pop('model_name')
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'model name is required')

    def test_without_model_id(self):
        data = self.data.copy()
        data.pop('model_id')
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, 'model id is required')

    def test_invalid_app_name(self):
        data = self.data.copy()
        val = 'not exists'
        data['app_name'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, f'{val} is not a valid app name')

    def test_invalid_model_name(self):
        data = self.data.copy()
        val = 'not exists'
        data['model_name'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.view.error, f'"{val}" is NOT a valid model name')

    def test_model_id_which_doesnt_exist(self):
        data = self.data.copy()
        val = 100
        data['model_id'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            self.view.error,
            f'"{val}" is NOT a valid model id for the model "{data["model_name"]}"')

    def test_non_integral_model_id(self):
        data = self.data.copy()
        val = 'c'
        data['model_id'] = val
        response = self.get_response(data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            self.view.error,
            f'model id must be an integer, "{val}" is NOT')

    def test_success(self):
        data = self.data.copy()
        data['model_id'] = str(data['model_id'])
        response = self.get_response(data)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.view.error)
        self.assertEqual(self.view.data, data)
        self.assertEqual(self.view.model_name, data['model_name'])
        self.assertEqual(self.view.app_name, data['app_name'])
        self.assertEqual(self.view.model_id, int(data['model_id']))
        self.assertEqual(self.view.model_obj, Post.objects.get(id=data['model_id']))
