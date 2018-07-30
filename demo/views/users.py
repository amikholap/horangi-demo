from demo.core.controllers.user import UserController
from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from ..serializers.users import UserSerializer


class UserListAPIView(DemoAPIView):

    controller = UserController.from_settings()

    def do_get(self, request):
        users = self.controller.user_dp.list()
        data = UserSerializer(users, many=True).data
        return DemoResponse(data)

    def do_post(self, request):
        username = request.arguments['username']
        user = self.controller.create_user(username=username)
        return DemoResponse(UserSerializer(user).data)

    def get_arguments_serializer_class(self, request):
        if request.method == 'POST':
            return UserSerializer
        return None
