from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views import View

from flag.mixins import ContentTypeMixin, RequestMixin
from flag.utils import get_model_object, process_flagging_request


class SetFlag(LoginRequiredMixin, RequestMixin, ContentTypeMixin, View):
    def post(self, request, *args, **kwargs):
        model_obj = get_model_object(
            app_name=self.app_name,
            model_name=self.model_name,
            model_id=self.mode_id
        )
        response = process_flagging_request(user=request.user, model_obj=model_obj, data=self.data)
        return JsonResponse(response)
