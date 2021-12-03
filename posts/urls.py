from django.contrib import admin
from django.urls import path, include

from .views import (ListPost, UserProfile, ListPostSubscriptions, FollowUser,
                    UnFollowUser, AddReadEnd, NewPost)

urlpatterns = [
    # Домашняяя станица
    path('', ListPost.as_view(), name='index'),
    # Новый пост
    path('new-posts', NewPost.as_view(), name='new-post'),
    # Профиль пользователей
    path('users/<str:username>/', UserProfile.as_view(), name='user-profile'),
    # Список постов на кого подписан
    path('subscriptions/', ListPostSubscriptions.as_view(),
         name='subscriptions'),
    # Подписка на пользователя
    path('<str:username>/follow/', FollowUser.as_view(), name='follow-user'),
    # Отписка от пользователя
    path('<str:username>/unfollow/', UnFollowUser.as_view(),
         name='un-follow-user'),
    # Добовление в прочитаное
    path('read-ends/<int:id>', AddReadEnd.as_view(), name='add-read-end'),
]