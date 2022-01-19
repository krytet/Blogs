import threading

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


def spam_massage(title, text, post):
    # Получение Email пользоветелей которые подписанны на создателя
    emails = list(post.author.writer.all().values_list('subscriber__email',
                                                       flat=True))
    send_mail(title, text, 'admin@blog.ru', emails)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='post', verbose_name='автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок поста')
    text = models.TextField(verbose_name='Тест поста')
    pub_date = models.DateTimeField(auto_now_add=True, blank=True,
                                    verbose_name='Дата и время создания')

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.id} {self.author}: {self.title}'


# Cигнал на создание/изменение поста
@receiver(post_save, sender=Post)
def create_post_profile(sender, instance, created, **kwargs):
    if created:
        title = f'У пользователя {instance.author} появился новый пост'
        text = f'У пользователя {instance.author} на которого вы подписаны' + \
               f', опубликован новый пост "{instance.title}" можете с ним ' + \
               f'ознакомся по ссылке <a href="/posts/{instance.id}/">' + \
               'кликни</a>'
    else:
        title = f'У пользователя {instance.author} изменился пост'
        text = f'У пользователя {instance.author} на которого вы подписаны' + \
               f', изменился пост "{instance.title}" можете с ним ' + \
               f'ознакомся по ссылке <a href="/posts/{instance.id}/">' + \
               'кликни</a>'
    th = threading.Thread(target=spam_massage(title, text, instance))
    th.start()


class Subscriptions(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='subscriber',
                                   verbose_name='Подписчик')
    writer = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='writer',
                               verbose_name='Писатель')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = 'subscriber', 'writer'

    def __str__(self):
        return f'{self.subscriber} подписан на {self.writer}'


class ReadEnd(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='read_end',
                               verbose_name='Читатель')
    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE,
                                     related_name='read_end',
                                     verbose_name='Подписка')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='read_end',
                             verbose_name='Прочтианый пост писателя')

    class Meta:
        verbose_name = 'Прочитаный пост'
        verbose_name_plural = 'Прочитаные посты'
        unique_together = 'author', 'subscription', 'post'

    def __str__(self):
        return f'{self.author} прочитал: {self.post}'
