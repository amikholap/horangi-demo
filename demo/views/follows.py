from demo.core.controllers.user import UserController
from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from ..serializers.users import FollowArgumentsSerializer


class BaseFollowAPIView(DemoAPIView):
    controller = UserController.from_settings()


class FollowApiView(BaseFollowAPIView):

    arguments_serializer_class = FollowArgumentsSerializer

    def do_post(self, request):
        error = None

        try:
            self.controller.follow(
                followee=request.arguments['followee'],
                follower=request.arguments['follower'],
            )
        except self.controller.Error as e:
            error = e.code

        return DemoResponse(errors=error)


class UnfollowApiView(BaseFollowAPIView):

    arguments_serializer_class = FollowArgumentsSerializer

    def do_post(self, request):
        error = None
        try:
            self.controller.unfollow(
                followee=request.arguments['followee'],
                follower=request.arguments['follower'],
            )
        except self.controller.Error as e:
            error = e.code
        return DemoResponse(errors=error)
