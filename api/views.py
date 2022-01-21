from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from posts.models import Post, ReadEnd, Subscriptions

from .filters import PostsFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializers, UserSerialiers

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiers
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    @action(methods=['GET', 'DELETE'], detail=True,
            permission_classes=[IsAuthenticated, ])
    def follow(self, request, *args, **kwargs):
        user = request.user
        writer = self.get_object()
        if request.method == 'GET':
            Subscriptions.objects.get_or_create(subscriber=user,
                                                writer=writer)
            return Response(status=status.HTTP_201_CREATED)
        else:
            subscription = get_object_or_404(Subscriptions,
                                             subscriber=user,
                                             writer=writer)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PostsFilter

    @action(methods=['GET'], detail=True, url_path='read-ends')
    def read_ends(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        follow = get_object_or_404(Subscriptions, subscriber=user,
                                   writer=post.author)
        ReadEnd.objects.get_or_create(author=user, subscription=follow,
                                      post=post)
        return Response(status=status.HTTP_201_CREATED)
