from .settings import *  # pylint: disable=unused-wildcard-import,wildcard-import


DATA_PROVIDERS = {
    'action': {
        'class': 'demo.core.data_providers.action.StubActionDataProvider',
        'params': {},
    },
    'follow': {
        'class': 'demo.core.data_providers.follow.StubFollowDataProvider',
        'params': {},
    },
    'user': {
        'class': 'demo.core.data_providers.user.StubUserDataProvider',
        'params': {},
    },
}
