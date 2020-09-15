from tests.base import BaseFlagMixinsTest, Client


class TestRequestMixin(BaseFlagMixinsTest):
    def test_non_ajax_response_post_required(self):
        response = self.request('post', self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Only POST AJAX requests are allowed')

    def test_ajax_get_request(self):
        self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.force_login(self.user_1)
        response = self.request('get', self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Only POST AJAX requests are allowed')


class TestContentTypeMixin(BaseFlagMixinsTest):
    def setUp(self):
        super().setUp()
        self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.client.force_login(self.user_1)

    def test_without_any_data(self):
        response = self.request('post', self.url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'no data passed')

    def test_with_invalid_data_format(self):
        response = self.client.generic('post', self.url, data='abcd')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode('utf-8'),
            'data sent is either empty or is not of an appropriate format')

    def test_without_app_name(self):
        data = self.data.copy()
        data.pop('app_name')
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'app name is required')

    def test_without_model_name(self):
        data = self.data.copy()
        data.pop('model_name')
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'model name is required')

    def test_without_model_id(self):
        data = self.data.copy()
        data.pop('model_id')
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'model id is required')

    def test_invalid_app_name(self):
        data = self.data.copy()
        val = 'not exists'
        data['app_name'] = val
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), f'{val} is not a valid app name')

    def test_invalid_model_name(self):
        data = self.data.copy()
        val = 'not exists'
        data['model_name'] = val
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), f'{val} is not a valid model name')

    def test_model_id_which_doesnt_exist(self):
        data = self.data.copy()
        val = 100
        data['model_id'] = val
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode('utf-8'),
            f'{val} is not a valid model id for the model {data["model_name"]}')

    def test_non_integral_model_id(self):
        data = self.data.copy()
        val = 'c'
        data['model_id'] = val
        response = self.request('post', self.url, data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content.decode('utf-8'),
            f'model id must be an integer, {val} is not')
