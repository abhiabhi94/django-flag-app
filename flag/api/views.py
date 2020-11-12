from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from flag.mixins import ContentTypeMixin
from flag.api.serializers import FlagSerializer
from flag.models import Flag
from flag.utils import process_flagging_request


class SetFlag(ContentTypeMixin, APIView):
    api = True
    permission_classes = (permissions.IsAuthenticated,)

    def _get_serializer_context(self):
        context = {}
        context['model_obj'] = self.model_obj
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        self.validate(self.request)
        response = process_flagging_request(user=request.user, model_obj=self.model_obj, data=self.data)
        detail = {'detail': response['msg']}

        if response['status']:  # 1 indicates bad request
            return Response(status=status.HTTP_400_BAD_REQUEST, data=detail)

        flag = Flag.objects.get_flag(self.model_obj)
        serializer = FlagSerializer(instance=flag, context=self._get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)
