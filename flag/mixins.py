from abc import ABCMeta, abstractmethod

from django.contrib.contenttypes.models import ContentType
from django.http import QueryDict
from django.http.response import JsonResponse
from django.utils.translation import gettext_lazy as _

from flag.exceptions import FlagBadRequest


class BaseMixin:
    __metaclass__ = ABCMeta
    api = False
    error = None

    def dispatch(self, request, *args, **kwargs):
        """
            Set `api=True` for rest framework.
            let rest framework handle the exception to choose the right renderer.
            validate method **should** be called in the derived API class.
        """
        if not self.api:
            try:
                self.validate(request)
            except FlagBadRequest as exc:
                return JsonResponse({'type': _('error'), 'detail': _(exc.detail)}, status=400)
        return super().dispatch(request, *args, **kwargs)

    @abstractmethod
    def validate(self, request, *args, **kwargs):
        pass

    def raise_error(self):
        raise FlagBadRequest(self.error)


class ContentTypeMixin(BaseMixin):
    model_obj = None
    data = None

    def _get_data_for_request(self, request):
        if self.api:
            data = request.POST or request.data
        else:
            data = request.POST

        if isinstance(data, QueryDict):
            return data.dict()
        return data

    def validate_data(self, request):
        data = self._get_data_for_request(request)
        if not data:
            self.error = 'no data passed'
            self.raise_error()
        return data

    def validate_app_name(self, app_name):
        if not app_name:
            self.error = 'app name is required'
            self.raise_error()

        if not ContentType.objects.filter(app_label=app_name).exists():
            self.error = f'{app_name} is not a valid app name'
            self.raise_error()

        return app_name

    def validate_model_name(self, model_name):
        if not model_name:
            self.error = 'model name is required'
            self.raise_error()

        return model_name

    def validate_model_id(self, model_id):
        if not model_id:
            self.error = 'model id is required'
            self.raise_error()
        try:
            model_id = int(model_id)
        except ValueError:
            self.error = f'model id must be an integer, "{model_id}" is NOT'
            self.raise_error()

        return model_id

    def validate_content_type_object(self, app_name, model_name):
        try:
            ct_object = ContentType.objects.get(model=model_name.lower(), app_label=app_name)
        except ContentType.DoesNotExist:
            self.error = f'"{model_name}" is NOT a valid model name'
            self.raise_error()

        return ct_object

    def validate_model_object(self, app_name, model_name, model_id):
        ct_object = self.validate_content_type_object(app_name, model_name)
        model_class = ct_object.model_class()
        model_query = model_class.objects.filter(id=model_id)
        if not model_query.exists() and model_query.count() != 1:
            self.error = f'"{model_id}" is NOT a valid model id for the model "{model_name}"'
            self.raise_error()
        return model_query.first()

    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        data = self.validate_data(request)
        app_name = data.get('app_name', None)
        self.app_name = self.validate_app_name(app_name)

        model_name = data.get('model_name', None)
        self.model_name = self.validate_model_name(model_name)

        model_id = data.get('model_id', None)
        self.model_id = self.validate_model_id(model_id)
        self.model_obj = self.validate_model_object(self.app_name, self.model_name, self.model_id)

        # initialize data to be used by view
        self.data = data


class AJAXMixin(BaseMixin):
    def validate(self, request, *args, **kwargs):
        super().validate(request, *args, **kwargs)
        if not request.META.get('HTTP_X_REQUESTED_WITH', None) == 'XMLHttpRequest':
            self.error = 'Only AJAX requests are allowed'
            self.raise_error()
