from django.urls import reverse

from demo.core.controllers.user import UserController
from demo.core.data_providers.user import StubUserDataProvider
from demo.drf.test import DemoAPITestCase


class UserListTestCase(DemoAPITestCase):

    @property
    def url(self):
        return reverse('api:user-list')

    def setUp(self):
        super().setUp()
        StubUserDataProvider.clear()

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


class FollowTestCase(DemoAPITestCase):

    @property
    def follow_url(self):
        return reverse('api:follow')

    @property
    def unfollow_url(self):
        return reverse('api:unfollow')

    def setUp(self):
        super().setUp()
        StubUserDataProvider.clear()
        controller = UserController.from_settings()
        controller.create_user(username='a')
        controller.create_user(username='b')

    def follow(self, followee, follower):
        data = {
            'followee': followee,
            'follower': follower,
        }
        return self.client.post(self.follow_url, data=data)

    def unfollow(self, followee, follower):
        data = {
            'followee': followee,
            'follower': follower,
        }
        return self.client.post(self.unfollow_url, data=data)

    def test_follow_nonexistent_followee(self):
        response = self.follow('c', 'a')
        self.assertResponseError(response, 'followee.invalid')

    def test_follow_nonexistent_follower(self):
        response = self.follow('a', 'c')
        self.assertResponseError(response, 'follower.invalid')

    def test_follow_ok(self):
        response = self.follow('a', 'b')
        self.assertResponseSuccess(response)

    def test_unfollow_nonexistent_followee(self):
        response = self.unfollow('c', 'b')
        self.assertResponseError(response, 'followee.invalid')

    def test_unfollow_nonexistent_follower(self):
        response = self.unfollow('a', 'c')
        self.assertResponseError(response, 'follower.invalid')

    def test_unfollow_not_followed(self):
        response = self.unfollow('a', 'b')
        self.assertResponseSuccess(response)

    def test_unfollow_ok(self):
        self.follow('a', 'b')
        response = self.unfollow('a', 'b')
        self.assertResponseSuccess(response)
