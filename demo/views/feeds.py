from demo.core.controllers.feed import FeedController
from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from ..serializers.actions import ActionFeedArgumentsSerializer, ActionSerializer


class BaseFeedAPIView(DemoAPIView):
    arguments_serializer_class = ActionFeedArgumentsSerializer
    controller = FeedController.from_settings()


class MyActionFeedAPIView(BaseFeedAPIView):

    def do_get(self, request):
        actions = self.controller.build_my_feed(
            actor=request.arguments['actor'],
            page=request.arguments['page'],
            page_size=request.arguments['page_size'],
        )
        data = ActionSerializer(actions, many=True).data
        return DemoResponse(data)


class FriendsActionFeedAPIView(BaseFeedAPIView):

    def do_get(self, request):
        actions = self.controller.build_friends_feed(
            username=request.arguments['actor'],
            page=request.arguments['page'],
            page_size=request.arguments['page_size'],
        )
        data = ActionSerializer(actions, many=True).data
        return DemoResponse(data)
