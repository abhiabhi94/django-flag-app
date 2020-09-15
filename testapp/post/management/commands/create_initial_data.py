from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand

from testapp.post.models import Post


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

    normal_user, _ = get_or_create('test', password='test')

    try:
        Post.objects.get(title='Test Post')
    except Post.DoesNotExist:
        Post.objects.create(title='Test Post', body='Hello django flag app', user=normal_user)
