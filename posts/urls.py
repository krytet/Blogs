from django.contrib import admin
from django.urls import path, include

from .views import (ListPost, UserProfile, ListPostSubscriptions, FollowUser,
                    UnFollowUser)

urlpatterns = [
    # Домашняяя станица
    path('', ListPost.as_view(), name='index'),
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

]