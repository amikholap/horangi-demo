from demo.core.controllers.action import ActionController
from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from ..serializers.actions import ActionArgumentsSerializer, ActionSerializer


class ActionListAPIView(DemoAPIView):

    arguments_serializer_class = ActionArgumentsSerializer

    controller = ActionController.from_settings()

    def do_post(self, request):
        # An improvement would be to pass action id from client to enable idempotent retries.

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
