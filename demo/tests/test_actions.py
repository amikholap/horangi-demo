from django.urls import reverse

from demo.core.controllers.user import UserController
from demo.core.data_providers.action import StubActionDataProvider
from demo.core.data_providers.user import StubUserDataProvider
from demo.drf.test import DemoAPITestCase


class CreateActionTestCaseMixin:

    @property
    def action_list_url(self):
        return reverse('api:action-list')

    def create_action(self, actor, target, verb='like', object_='post:1', check_success=True):
        data = {
            'actor': actor,
            'verb': verb,
            'object': object_,
            'target': target,
        }
        response = self.client.post(self.action_list_url, data=data)
        if check_success:
            self.assertResponseSuccess(response)
        return response


class CreateActionTestCase(CreateActionTestCaseMixin, DemoAPITestCase):

    def setUp(self):
        StubActionDataProvider.clear()
        StubUserDataProvider.clear()

        self.controller = UserController.from_settings()
        self.controller.create_user(username='a')

    def test_ok(self):
        response = self.create_action(actor='a', target='a')
        data = response.data['data']
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_invalid_actor(self):
        response = self.create_action(actor='z', target='a', check_success=False)
        self.assertResponseError(response, 'actor.invalid')

    def test_invalid_target(self):
        response = self.create_action(actor='a', target='z', check_success=False)
        self.assertResponseError(response, 'target.invalid')
