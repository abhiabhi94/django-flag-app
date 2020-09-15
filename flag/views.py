from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from flag.mixins import ContentTypeMixin, RequestMixin
from flag.models import Flag, FlagInstance
from flag.utils import get_model_object


class SetFlag(LoginRequiredMixin, RequestMixin, ContentTypeMixin, View):
    def post(self, request, *args, **kwargs):
        response = {'status': 1}
        model_obj = get_model_object(
            app_name=self.app_name,
            model_name=self.model_name,
            model_id=self.mode_id
        )
        flag = Flag.objects.get_flag(model_obj)

        try:
            if FlagInstance.objects.set_flag(request.user, flag, **self.data):
                response['msg'] = _(
                    'The content has been flagged successfully. '
                    'A moderator will review it shortly.'
                    )
                response['flag'] = 1
            else:
                response['msg'] = _('The content has been unflagged successfully.')

            response.update({
                'status': 0
            })
        except ValidationError as e:
            response.update({
                'msg': e.messages
            })

        return JsonResponse(response)
