from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.views import View

from flag.mixins import AJAXMixin, ContentTypeMixin
from flag.utils import process_flagging_request


class SetFlag(LoginRequiredMixin, ContentTypeMixin, AJAXMixin, View):
    def post(self, request, *args, **kwargs):
        response = process_flagging_request(user=request.user, model_obj=self.model_obj, data=self.data)
        return JsonResponse(response)
