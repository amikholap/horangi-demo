from django.conf import settings

from ..data_providers.base import BaseDataProvider
from .base import BaseController


class FeedController(BaseController):

    class Error(Exception):
        def __init__(self, code):
            super().__init__(code)
            self.code = code

    @classmethod
    def from_settings(cls):
        action_dp = BaseDataProvider.from_settings(settings.DATA_PROVIDERS['action'])
        follow_dp = BaseDataProvider.from_settings(settings.DATA_PROVIDERS['follow'])
        return cls(
            action_data_provider=action_dp,
            follow_data_provider=follow_dp,
        )

    def __init__(self, action_data_provider, follow_data_provider):
        self.action_dp = action_data_provider
        self.follow_dp = follow_data_provider

    def build_my_feed(self, actor, page, page_size):
        # Should be ok to query DB on each access.
        # The operation touches only one partition and is probably not very frequent.
        return self.action_dp.list(
            actor_username=actor,
            page=page,
            page_size=page_size,
        )

    def build_friends_feed(self, username, page, page_size):  # pylint: disable=unused-argument
        # Should be cached.
        # The cache can be updated by a process
        #   that listens for follow/unfollow events on a queue.
        followees = self.follow_dp.get_followees(username)

        # First couple of pages should be cached as well.
        # Requests for further pages would resort to DB access.
        actions = self.action_dp.list(followees, page=page, page_size=page_size)

        return actions
