from django.conf import settings

from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from demo.util import import_class
from ..serializers.users import UserSerializer


class UserListAPIView(DemoAPIView):

    data_provider_class = import_class(settings.APP['users']['data_provider']['class'])
    data_provider = data_provider_class(**settings.APP['users']['data_provider']['params'])

    def do_get(self, request):
        users = self.data_provider.get_users()
        data = UserSerializer(users, many=True).data
        return DemoResponse(data)

    def do_post(self, request):
        username = request.arguments['username']
        user = self.data_provider.create_user(username=username)
        return DemoResponse(UserSerializer(user).data)

    def get_arguments_serializer_class(self, request):
        if request.method == 'POST':
            return UserSerializer
        return None
