from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model

from .models import Post, Subscriptions, ReadEnd

User = get_user_model()

class ListPost(ListView):

    model = Post
    queryset = Post.objects.all()
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-id']


class UserProfile(DetailView):

    model = User
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = kwargs
        print(self.request.user)
        user = kwargs['object']
        context['posts'] = user.post.all()
        context['user'] = kwargs['object']
        return context


class ListPostSubscriptions(ListView):

    model = Post
    queryset = Post.objects.all()
    template_name = 'users/subscriptions.html'
    context_object_name = 'posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        user = self.request.user
        posts = Post.objects.filter(author__writer__subscriber=user)
        context = super().get_context_data(**kwargs)
        context['posts'] = posts
        print(posts)
        print(kwargs)
        print(super().get_context_data(**kwargs))
        return context


        