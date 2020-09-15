from rest_framework import serializers

from testapp.post.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.HyperlinkedRelatedField(
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
            'author',
        )

    @staticmethod
    def get_slug(obj):
        return str(obj.slug)
