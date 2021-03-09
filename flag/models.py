from collections import namedtuple
from enum import IntEnum, unique

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from flag.managers import FlagInstanceManager, FlagManager
from flag.conf import settings

User = settings.AUTH_USER_MODEL


class Flag(models.Model):
    """Used to add flag/moderation to a model"""
    @unique
    class State(IntEnum):
        UNFLAGGED = 1
        FLAGGED = 2
        REJECTED = 3
        NOTIFIED = 4
        RESOLVED = 5

    STATE_CHOICES = [
        (State.UNFLAGGED.value, _('Unflagged')),
        (State.FLAGGED.value, _('Flagged')),
        (State.REJECTED.value, _('Flag rejected by the moderator')),
        (State.RESOLVED.value, _('Content modified by the author')),
        (State.NOTIFIED.value, _('Creator notified')),
    ]

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creator = models.ForeignKey(User, related_name='flags_against', null=True, on_delete=models.CASCADE)
    state = models.SmallIntegerField(choices=STATE_CHOICES, default=State.UNFLAGGED.value)
    moderator = models.ForeignKey(User, null=True, related_name='flags_moderated', on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(default=0)

    objects = FlagManager()

    class Meta:
        verbose_name = _('Flag')
        unique_together = ['content_type', 'object_id']

    def increase_count(self):
        field = 'count'
        self.refresh_from_db()
        self.count = models.F(field) + 1
        self.save(update_fields=[field])

    def decrease_count(self):
        field = 'count'
        self.refresh_from_db()
        self.count = models.F(field) - 1
        self.save(update_fields=[field])

    def get_clean_state(self, state):
        err = ValidationError(_('%(state)s is an invalid state'), code='invalid', params={'state': state})
        try:
            state = int(state)
            if state not in [st.value for st in self.State]:
                raise err
        except (ValueError, TypeError):
            raise err
        return state

    def get_verbose_state(self, state):
        state = self.get_clean_state(state)
        for item in self.STATE_CHOICES:
            if item[0] == state:
                return item[1]

    def toggle_state(self, state, moderator):
        state = self.get_clean_state(state)
        # toggle states occurs between rejected and resolved states only
        if state != self.State.REJECTED.value and state != self.State.RESOLVED.value:
            raise ValidationError(_('%(state)s is an invalid state'), code='invalid', params={'state': state})
        if self.state == state:
            self.state = self.State.FLAGGED.value
        else:
            self.state = state
        self.moderator = moderator
        self.save()

    def toggle_flagged_state(self):
        allowed_flags = settings.FLAG_ALLOWED
        self.refresh_from_db()
        field = 'state'
        if self.count > allowed_flags and (
            getattr(self, field) not in [self.State.RESOLVED.value, self.State.REJECTED.value]
        ):
            setattr(self, field, self.State.FLAGGED.value)
        else:
            setattr(self, field, self.State.UNFLAGGED.value)
        self.save(update_fields=[field])

    @property
    def is_flagged(self):
        return self.state != self.State.UNFLAGGED.value


class FlagInstance(models.Model):
    REASON = settings.FLAG_REASONS

    REASON.append((100, _('Something else')))

    # Make a named tuple
    Reasons = namedtuple('Reason', ['value', 'reason'])

    # Construct the list of named tuples
    reasons = []
    for reason in REASON:
        reasons.append(Reasons(*reason))

    reason_values = [reason.value for reason in reasons]

    flag = models.ForeignKey(Flag, related_name='flags', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='flags_by', on_delete=models.CASCADE)
    date_flagged = models.DateTimeField(auto_now_add=timezone.now)
    reason = models.SmallIntegerField(choices=REASON, default=reason_values[0])
    info = models.TextField(null=True, blank=True)

    objects = FlagInstanceManager()

    class Meta:
        verbose_name = _('Flag Instance')
        verbose_name_plural = _('Flag Instances')
        unique_together = ['flag', 'user']
        ordering = ['-date_flagged']

    def clean(self):
        """If something else is choosen, info shall not be empty"""
        if self.reason == self.reason_values[-1] and not self.info:
            raise ValidationError(
                {
                    'info': ValidationError(
                        _('Please provide some information why you choose to report the content'),
                        code='required')
                }
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(FlagInstance, self).save(*args, **kwargs)
