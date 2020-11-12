from django.contrib.auth import get_user_model
from rest_framework import serializers

from flag.models import Flag


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        lookup_field = 'username'


class FlagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flag
        fields = ('creator', 'count', 'state', 'verbose_state', 'moderator', 'is_flagged', 'reporters')
        read_only_fields = ('creator', 'moderator', 'reporters')

    creator = UserSerializer()
    moderator = UserSerializer()
    verbose_state = serializers.SerializerMethodField()
    reporters = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        context = kwargs['context']
        self.model_obj = context.get('model_obj')
        self.user = context.get('user')
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_verbose_state(obj):
        return obj.get_verbose_state(obj.state)

    def get_reporters(self, obj):
        flag_obj = Flag.objects.get_flag(self.model_obj)
        return [
            {'id': instance.user.id, 'username': instance.user.username} for instance in flag_obj.flags.all()
        ]
