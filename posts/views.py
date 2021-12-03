from django.shortcuts import redirect, render
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
        posts = Post.objects.filter(author__writer__subscriber=user).order_by('-id')
        #context = {}
        context = super().get_context_data(**kwargs)
        context['posts'] = posts
        print(posts)
        print(kwargs)
        print(super().get_context_data(**kwargs))
        return context


# Подписка на пользователей
class FollowUser(DetailView):

    model = User
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        print(request.user)
        Subscriptions.objects.get_or_create(subscriber=request.user,
                                            writer=user)
        return redirect(f'/users/{user.username}/')
    

# Отписка от пользователя
class UnFollowUser(DetailView):
    
    model = User
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        print(request.user)
        follow = Subscriptions.objects.get(subscriber=request.user, writer=user)
        follow.delete()
        return redirect(f'/users/{user.username}/')
