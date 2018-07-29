from django.urls import reverse

from demo.core.users import StubUsersDataProvider
from demo.drf.test import DemoAPITestCase


class UserListTestCase(DemoAPITestCase):

    @property
    def url(self):
        return reverse('api:user-list')

    def setUp(self):
        super().setUp()
        StubUsersDataProvider.clear()

    def test_empty(self):
        response = self.client.get(self.url)
        self.assertResponseSuccess(response)
        self.assertResponseDataEqual(response, [])

    def test_create_no_username(self):
        response = self.client.post(self.url, json={})
        self.assertResponseError(response, 'username.required')

    def test_create_ok(self):
        create_response = self.client.post(self.url, data={'username': 'alex'})
        self.assertResponseSuccess(create_response)
        list_response = self.client.get(self.url)
        self.assertResponseDataEqual(list_response, [{'username': 'alex'}])
