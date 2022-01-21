from django_filters import rest_framework as filters
from django_filters.filters import BooleanFilter

from posts.models import Post


class PostsFilter(filters.FilterSet):
    follow = BooleanFilter(method='get_posts_follow')

    class Meta:
        model = Post
        fields = ['follow']

    def get_posts_follow(self, obj, name, value):
        user = self.request.user
        if value:
            return obj.filter(author__writer__subscriber=user).order_by('-id')
        else:
            return obj.exclude(author__writer__subscriber=user).order_by('-id')
