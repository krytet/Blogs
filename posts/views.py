from django.shortcuts import get_object_or_404, redirect, render
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
        # добавление временной переменной о состояни прочтения
        for i in range(len(posts)):
            if posts[i].read_end.all().filter(author=user).exists():
                posts[i].read = True
            else:
                posts[i].read = False
        context = super().get_context_data(**kwargs)
        context['posts'] = posts
        context['user'] = user
        return context


# Подписка на пользователей
class FollowUser(DetailView):

    model = User
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
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
        follow = Subscriptions.objects.get(subscriber=request.user, writer=user)
        follow.delete()
        return redirect(f'/users/{user.username}/')


# Добавление в прочитанное
class AddReadEnd(DetailView):

    model = Post
    queryset = Post.objects.all()
    slug_field = 'id'
    slug_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        follow = get_object_or_404(Subscriptions, subscriber=user,
                                   writer=post.author)
        ReadEnd.objects.get_or_create(author=user, subscription=follow,
                                      post=post)
        return redirect('subscriptions')