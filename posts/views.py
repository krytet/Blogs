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
        user = kwargs['object']
        context['posts'] = user.post.all()
        context['user'] = kwargs['object']
        return context