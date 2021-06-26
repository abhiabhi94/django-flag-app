import sys

from django.db import migrations
from django.utils.translation import gettext_lazy as _
from django.core.management import color_style

from django.apps import apps


POST_TITLE = _('Test Post for django-flag-app')
style = color_style(force_color=True)


def _generate_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Post = apps.get_model('post', 'Post')

    def _get_or_create_user(username, password):
        created = False
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create(username=username, password=password)
            created = True
        return user, created

    moderator, created = _get_or_create_user('moderator', password='moderator')
    if created:
        moderator_group, __ = Group.objects.get_or_create(name='flag_moderator')
        moderator_group.user_set.add(moderator)

    user, __ = _get_or_create_user('test', password='test')
    admin_user, created_super_user = _get_or_create_user('admin', password='admin')
    if created_super_user:
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

    # the create method here doesn't call save weirdly here, so slug is passed manually
    Post.objects.create(
        title=POST_TITLE,
        body=_('Hello django flag app'),
        user=user,
        slug='test-post',
    )

    sys.stdout.write(style.SUCCESS(_('Initial data created successfully.')))


def _destroy_initial_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Post = apps.get_model('post', 'Post')

    def delete(objs):
        if objs:
            objs.delete()

    delete(Post.objects.filter(title=POST_TITLE))
    users = User.objects.filter(username__in=['test', 'admin', 'moderator'])
    delete(users)
    delete(Group.objects.filter(name='flag_moderator'))

    sys.stdout.write(style.WARNING(_('Initial data deleted successfully')))


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_generate_initial_data, reverse_code=_destroy_initial_data),
    ]
