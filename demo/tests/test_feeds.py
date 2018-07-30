from django.urls import reverse

from demo.core.controllers.user import UserController
from demo.core.data_providers.action import StubActionDataProvider
from demo.core.data_providers.follow import StubFollowDataProvider
from demo.core.data_providers.user import StubUserDataProvider
from demo.drf.test import DemoAPITestCase

from .test_actions import CreateActionTestCaseMixin


class MyFeedTestCase(CreateActionTestCaseMixin, DemoAPITestCase):

    @property
    def url(self):
        return reverse('api:my-feed')

    def setUp(self):
        StubActionDataProvider.clear()
        StubFollowDataProvider.clear()
        StubUserDataProvider.clear()

        self.controller = UserController.from_settings()
        self.controller.create_user(username='a')
        self.controller.create_user(username='b')

    def get_feed(self, actor, page=None, page_size=None):
        data = {
            'actor': actor,
        }
        if page is not None:
            data['page'] = str(page)
        if page_size is not None:
            data['page_size'] = str(page_size)
        return self.client.get(self.url, data=data)

    def test_empty(self):
        response = self.get_feed(actor='a')
        self.assertResponseSuccess(response)
        self.assertResponseDataEqual(response, [])

    def test_nonexistent_actor(self):
        response = self.get_feed(actor='z')
        self.assertResponseSuccess(response)
        self.assertResponseDataEqual(response, [])

    def test_one_action(self):
        self.create_action(actor='a', target='b')

        response = self.get_feed(actor='a')
        self.assertResponseSuccess(response)

        data = response.data['data']
        self.assertEqual(len(data), 1)

        action_data = data[0]
        self.assertEqual(action_data['actor'], 'a')
        self.assertEqual(action_data['target'], 'b')

    def test_other_user_action(self):
        self.create_action(actor='a', target='b')
        response = self.get_feed(actor='b')
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 0)

    def test_first_page(self):
        self.create_action(actor='a', target='b')
        response = self.get_feed(actor='a', page=0)
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 1)

    def test_large_page(self):
        self.create_action(actor='a', target='b')
        response = self.get_feed(actor='a', page=777)
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 0)

    def test_multiple_pages(self):
        page_size = 10
        for _ in range(2 * page_size + 1):
            self.create_action(actor='a', target='b')

        response_page0 = self.get_feed(actor='a', page=0, page_size=page_size)
        response_page1 = self.get_feed(actor='a', page=1, page_size=page_size)
        response_page2 = self.get_feed(actor='a', page=2, page_size=page_size)
        response_page3 = self.get_feed(actor='a', page=3, page_size=page_size)

        self.assertResponseSuccess(response_page0)
        self.assertResponseSuccess(response_page1)
        self.assertResponseSuccess(response_page2)
        self.assertResponseSuccess(response_page3)

        self.assertEqual(len(response_page0.data['data']), page_size)
        self.assertEqual(len(response_page1.data['data']), page_size)
        self.assertEqual(len(response_page2.data['data']), 1)


class FriendsFeedTestCase(CreateActionTestCaseMixin, DemoAPITestCase):

    @property
    def url(self):
        return reverse('api:friends-feed')

    def setUp(self):
        StubActionDataProvider.clear()
        StubUserDataProvider.clear()

        self.controller = UserController.from_settings()
        self.controller.create_user(username='a')
        self.controller.create_user(username='b')

        # b follows a.
        self.controller.follow(followee='a', follower='b')

    def get_feed(self, actor, page=None, page_size=None):
        data = {
            'actor': actor,
        }
        if page is not None:
            data['page'] = str(page)
        if page_size is not None:
            data['page_size'] = str(page_size)
        return self.client.get(self.url, data=data)

    def test_empty(self):
        response = self.get_feed(actor='a')
        self.assertResponseSuccess(response)
        self.assertResponseDataEqual(response, [])

    def test_nonexistent_actor(self):
        response = self.get_feed(actor='z')
        self.assertResponseSuccess(response)
        self.assertResponseDataEqual(response, [])

    def test_one_action(self):
        self.create_action(actor='b', target='a')
        response = self.get_feed(actor='a')
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 0)

    def test_one_action_reverse(self):
        self.create_action(actor='a', target='b')

        response = self.get_feed(actor='b')
        self.assertResponseSuccess(response)

        data = response.data['data']
        self.assertEqual(len(data), 1)

        action_data = data[0]
        self.assertEqual(action_data['actor'], 'a')
        self.assertEqual(action_data['target'], 'b')

    def test_self_action(self):
        self.create_action(actor='a', target='b')
        response = self.get_feed(actor='a')
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 0)

    def test_first_page(self):
        self.create_action(actor='a', target='b')
        response = self.get_feed(actor='b', page=0)
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 1)

    def test_large_page(self):
        self.create_action(actor='a', target='b')
        response = self.get_feed(actor='b', page=777)
        self.assertResponseSuccess(response)
        self.assertEqual(len(response.data['data']), 0)

    def test_multiple_pages(self):
        page_size = 10
        for _ in range(2 * page_size + 1):
            self.create_action(actor='a', target='b')

        response_page0 = self.get_feed(actor='b', page=0, page_size=page_size)
        response_page1 = self.get_feed(actor='b', page=1, page_size=page_size)
        response_page2 = self.get_feed(actor='b', page=2, page_size=page_size)
        response_page3 = self.get_feed(actor='b', page=3, page_size=page_size)

        self.assertResponseSuccess(response_page0)
        self.assertResponseSuccess(response_page1)
        self.assertResponseSuccess(response_page2)
        self.assertResponseSuccess(response_page3)

        self.assertEqual(len(response_page0.data['data']), page_size)
        self.assertEqual(len(response_page1.data['data']), page_size)
        self.assertEqual(len(response_page2.data['data']), 1)
        self.assertEqual(len(response_page3.data['data']), 0)
        self.assertEqual(len(response_page3.data['data']), 0)
