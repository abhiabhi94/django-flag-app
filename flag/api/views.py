from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from flag.mixins import ContentTypeMixin
from flag.utils import get_model_object, process_flagging_request


class SetFlag(ContentTypeMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        model_obj = get_model_object(
            app_name=self.app_name,
            model_name=self.model_name,
            model_id=self.mode_id
        )
        response = process_flagging_request(user=request.user, model_obj=model_obj, data=self.data)
        detail = {'detail': response['msg']}

        if response['status']:  # 1 indicates bad request
            return Response(status=status.HTTP_400_BAD_REQUEST, data=detail)

        if response.get('flag', None):
            return Response(status=status.HTTP_201_CREATED, data=detail)

        return Response(status=status.HTTP_200_OK, data=detail)
