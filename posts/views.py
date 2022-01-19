from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .models import Post, ReadEnd, Subscriptions

User = get_user_model()


# Создание нового поста
class NewPost(LoginRequiredMixin, CreateView):

    model = Post
    fields = ['title', 'text']
    template_name = 'posts/new_post.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Вывод список новых постов
class ListPost(ListView):

    model = Post
    queryset = Post.objects.all()
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-id']


# Вывод определенного поста
class PostView(DetailView):

    model = Post
    queryset = Post.objects.all()
    template_name = 'posts/post-detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = context['posts'].author
        return context


# Вывод постов пользователя
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
        context['user_profile'] = kwargs['object']
        if self.request.user.is_authenticated:
            following = Subscriptions.objects.filter(
                                                 subscriber=self.request.user,
                                                 writer=user)
            context['following'] = following
        return context


# Вывод новых постов подписок
class ListPostSubscriptions(LoginRequiredMixin, ListView):

    model = Post
    queryset = Post.objects.all()
    template_name = 'users/subscriptions.html'
    context_object_name = 'posts'
    ordering = ['-id']

    def get_context_data(self, **kwargs):
        user = self.request.user
        posts = Post.objects.filter(author__writer__subscriber=user) \
                    .order_by('-id')
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


# Подписка/Отписка на пользователей
class FollowUser(LoginRequiredMixin, DetailView):

    model = User
    queryset = User.objects.all()
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        subscription, is_create = Subscriptions.objects.get_or_create(
            subscriber=request.user,
            writer=user
        )
        # если есть подписка то удаляем
        if not is_create:
            subscription.delete()
        return redirect(f'/users/{user.username}/')


# Добавление в прочитанное
class AddReadEnd(LoginRequiredMixin, DetailView):

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
