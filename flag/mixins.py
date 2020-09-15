import json

from django.contrib.contenttypes.models import ContentType

from flag.exceptions import FlagBadRequest


class ContentTypeMixin:
    def dispatch(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return FlagBadRequest('data sent is either empty or is not of an appropriate format')
        if not data:
            return FlagBadRequest('no data passed')

        app_name = data.get('app_name', None)
        if not app_name:
            return FlagBadRequest('app name is required')

        model_name = data.get('model_name', None)
        if not model_name:
            return FlagBadRequest('model name is required')

        model_id = data.get('model_id', None)
        if not model_id:
            return FlagBadRequest('model id is required')

        if not ContentType.objects.filter(app_label=app_name).exists():
            return FlagBadRequest(f'{app_name} is not a valid app name')

        try:
            ctype = ContentType.objects.get(model=model_name.lower()).model_class()
            model_class = ctype.objects.filter(id=model_id)
            if not model_class.exists() and model_class.count() != 1:
                return FlagBadRequest(f'{model_id} is not a valid model id for the model {model_name}')

        except ContentType.DoesNotExist:
            return FlagBadRequest(f'{model_name} is not a valid model name')

        except ValueError:
            return FlagBadRequest(f'model id must be an integer, {model_id} is not')

        self.app_name = app_name
        self.model_name = model_name
        self.mode_id = model_id
        self.data = data
        return super().dispatch(request, *args, **kwargs)


class RequestMixin:
    def dispatch(self, request, *args, **kwargs):
        if (not request.META.get('HTTP_X_REQUESTED_WITH', None) == 'XMLHttpRequest') or (not request.method == 'POST'):
            return FlagBadRequest('Only POST AJAX requests are allowed')

        return super().dispatch(request, *args, **kwargs)
