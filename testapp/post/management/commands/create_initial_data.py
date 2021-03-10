from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from testapp.post.models import Post


class Command(BaseCommand):
    help = _("Generate initial data")

    @staticmethod
    def __get_or_create(username, password):
        created = False
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            created = True
        return user, created

    def __generate_initial_data(self):
        moderator, created = self.__get_or_create('moderator', password='moderator')
        if created:
            moderator_group, __ = Group.objects.get_or_create(name='flag_moderator')
            moderator_group.user_set.add(moderator)

        user, __ = self.__get_or_create('test', password='test')
        admin_user, created_super_user = self.__get_or_create('admin', password='admin')
        if created_super_user:
            admin_user.is_staff = True
            admin_user.save()

        try:
            Post.objects.get(title=_('Test Post'))
            self.stdout.write(self.style.WARNING(_('Initial data already present.')))

        except Post.DoesNotExist:
            Post.objects.create(
                title=_('Test Post'), body=_('Hello django flag app'), user=user)
            self.stdout.write(self.style.SUCCESS(_('Initial data created successfully.')))

    def handle(self, *args, **options):
        self.__generate_initial_data()
