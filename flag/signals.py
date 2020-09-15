from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from flag.models import Flag, FlagInstance


@receiver(post_save, sender=FlagInstance)
def flagged(sender, instance, created, raw, using, update_fields, **kwargs):
    """Increase flag count in the flag model after creating an instance"""
    if created:
        instance.flag.increase_count()
        instance.flag.toggle_flagged_state()


@receiver(post_delete, sender=FlagInstance)
def unflagged(sender, instance, using, **kwargs):
    """Decrease flag count in the flag model before deleting an instance"""
    instance.flag.decrease_count()
    instance.flag.toggle_flagged_state()


def create_permission_groups(sender, **kwargs):
    flag_ct = ContentType.objects.get_for_model(Flag)
    delete_flagged_perm, __ = Permission.objects.get_or_create(
        codename='delete_flagged_content',
        name=_('Can delete flagged content'),
        content_type=flag_ct
    )
    moderator_group, __ = Group.objects.get_or_create(name='flag_moderator')
    moderator_group.permissions.add(delete_flagged_perm)


def adjust_flagged_content(sender, **kwargs):
    for flag in Flag.objects.all():
        flag.toggle_flagged_state()
