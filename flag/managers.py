from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

from flag.utils import get_content_type, get_user_for_model


class FlagManager(models.Manager):
    def get_flag(self, model_obj):
        ctype = get_content_type(model_obj)
        creator = get_user_for_model(model_obj)
        flag, __ = self.get_or_create(content_type=ctype, object_id=model_obj.id, creator=creator)
        return flag

    def is_flagged(self, model_obj):
        flag = self.get_flag(model_obj)
        return flag.is_flagged

    def has_flagged(self, user, model_obj):
        """
        Returns whether a model object has been flagged by a user or not

        Args:
            user (object): the user to be inquired about.
            model_obj (object): the model object to be inquired upon.

        Returns:
            bool
        """
        flag = self.get_flag(model_obj)
        return flag.flags.filter(user=user).exists()


class FlagInstanceManager(models.Manager):
    def _clean_reason(self, reason):
        err = ValidationError(
                _('%(reason)s is an invalid reason'),
                params={'reason': reason},
                code='invalid'
                )
        try:
            reason = int(reason)
            if reason in self.model.reason_values:
                return reason
            raise err

        except (ValueError, TypeError):
            raise err

    def _clean(self, reason, info):
        cleaned_reason = self._clean_reason(reason)
        cleaned_info = None

        if cleaned_reason == self.model.reason_values[-1]:
            cleaned_info = info
            if not cleaned_info:
                raise ValidationError(
                    _('Please supply some information as the reason for flagging'),
                    params={'info': info},
                    code='required'
                )
        return cleaned_reason, cleaned_info

    def create_flag(self, user, flag, reason, info):
        cleaned_reason, cleaned_info = self._clean(reason, info)
        try:
            self.create(flag=flag, user=user, reason=cleaned_reason, info=cleaned_info)
        except IntegrityError:
            raise ValidationError(
                    _('This content has already been flagged by the user (%(user)s)'),
                    params={'user': user},
                    code='invalid'
                )

    def delete_flag(self, user, flag):
        try:
            self.get(user=user, flag=flag).delete()
        except self.model.DoesNotExist:
            raise ValidationError(
                _('This content has not been flagged by the user (%(user)s)'),
                params={'user': user},
                code='invalid'
            )

    def set_flag(self, user, model_obj, **kwargs):
        Flag = apps.get_model('flag', 'Flag')
        flag_obj = Flag.objects.get_flag(model_obj)
        info = kwargs.get('info', None)
        reason = kwargs.get('reason', None)

        if reason:
            self.create_flag(user, flag_obj, reason, info)
            created = True
        else:
            self.delete_flag(user, flag_obj)
            created = False

        return created
