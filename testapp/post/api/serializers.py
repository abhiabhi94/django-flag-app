from rest_framework import serializers

from testapp.post.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        lookup_field='username',
    )
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'slug',
            'title',
            'body',
            'date',
            'editdate',
            'user',
        )

    @staticmethod
    def get_slug(obj):
        return str(obj.slug)
