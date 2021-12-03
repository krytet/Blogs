from typing import Callable
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='post', verbose_name='автор'
                               )
    title = models.CharField(max_length=255, verbose_name='Заголовок поста')
    text = models.TextField(verbose_name='Тест поста')
    pub_date = models.DateTimeField(auto_now_add=True, blank=True,
                                    verbose_name='Дата и время создания'
                                    )

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
    
    def __str__(self):
        return f'{self.id} {self.author}: {self.title}'


class Subscriptions(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='subscriber',
                                   verbose_name='Подписчик'
                                   )
    writer = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='writer',
                               verbose_name='Писатель'
                               )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
    
    def __str__(self):
        return f'{self.subscriber} подписан на {self.writer}'


class ReadEnd(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='read_end',
                               verbose_name='Читатель'
                               )
    subscription = models.ForeignKey(Subscriptions, on_delete=models.CASCADE,
                                     related_name='read_end',
                                     verbose_name='Подписка'
                                     )
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='read_end',
                             verbose_name='Прочтианый пост писателя'
                             )

    class Meta:
        verbose_name = 'Прочитаный пост'
        verbose_name_plural = 'Прочитаные посты'
    
    def __str__(self):
        return f'{self.author} прочитал: {self.post}'
