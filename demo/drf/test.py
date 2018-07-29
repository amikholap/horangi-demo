from rest_framework.test import APITestCase


class DemoAPITestCase(APITestCase):

    def assertResponseOk(self, response):
        self.assertEqual(response.status_code // 100, 2, response.status_code)

    def assertResponseSuccess(self, response):
        self.assertResponseOk(response)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('status'), 'success', response.data)

    def assertResponseError(self, response, code=None):
        self.assertResponseOk(response)
        self.assertIsNotNone(response.data)
        self.assertEqual(response.data.get('status'), 'error', response.data)
        self.assertIn('errors', response.data, response.data)
        if code:
            self.assertIn(code, response.data['errors'], response.data)

    def assertResponseDataEqual(self, response, data):
        self.assertEqual(response.data.get('data'), data, response.data)
