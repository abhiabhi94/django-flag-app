from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from testapp.post.models import Post


User = get_user_model()


class Command(BaseCommand):
    help = "Generate initial data"

    def handle(self, *args, **options):
        generate_initial_data()


def get_or_create(username, password):
    created = False
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password)
        created = True
    return user, created


def generate_initial_data():
    moderator, created = get_or_create('moderator', password='moderator')
    if created:
        moderator_group, _ = Group.objects.get_or_create(name='flag_moderator')
        moderator_group.user_set.add(moderator)

    user, _ = get_or_create('test', password='test')
    admin_user, created_super_user = get_or_create('admin', password='admin')
    if created_super_user:
        admin_user.is_staff = True
        admin_user.save()

    try:
        Post.objects.get(title='Test Post')
    except Post.DoesNotExist:
        Post.objects.create(title='Test Post', body='Hello django flag app', user=user)
