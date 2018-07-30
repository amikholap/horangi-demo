from demo.core.controllers.action import ActionController
from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from ..serializers.actions import (
    ActionArgumentsSerializer, ActionFeedArgumentsSerializer, ActionSerializer,
)


class BaseActionAPIView(DemoAPIView):
    controller = ActionController.from_settings()


class ActionListAPIView(BaseActionAPIView):

    arguments_serializer_class = ActionArgumentsSerializer

    def do_post(self, request):
        # An improvement would be to provide action id by the client to enable idempotent retries.

        data = None
        error = None

        try:
            action = self.controller.create_action(
                actor=request.arguments['actor'],
                verb=request.arguments['verb'],
                object_=request.arguments['object'],
                target=request.arguments['target'],
            )
        except self.controller.Error as e:
            error = e.code

        if error is None:
            data = ActionSerializer(action).data

        return DemoResponse(data=data, errors=error)


class MyActionFeedAPIView(BaseActionAPIView):

    arguments_serializer_class = ActionFeedArgumentsSerializer

    def do_get(self, request):
        actions = self.controller.action_dp.list(
            actor_username=request.arguments['actor'],
            page=request.arguments['page'],
            page_size=request.arguments['page_size'],
        )
        data = ActionSerializer(actions, many=True).data
        return DemoResponse(data)
