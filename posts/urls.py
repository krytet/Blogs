from django.urls import path

from .views import (AddReadEnd, FollowUser, ListPost, ListPostSubscriptions,
                    NewPost, PostView, UserProfile)

urlpatterns = [
    # Домашняяя станица
    path('', ListPost.as_view(), name='index'),
    # Новый пост
    path('posts/create/', NewPost.as_view(), name='new-post'),
    # Просмотр поста
    path('posts/<int:id>/', PostView.as_view(), name='post-detail'),
    # Добовление в прочитаное
    path('posts/<int:id>/read-ends/', AddReadEnd.as_view(),
         name='add-read-end'),
    # Профиль пользователей
    path('users/<str:username>/', UserProfile.as_view(), name='user-profile'),
    # Подписка/Отписка на пользователя
    path('users/<str:username>/follow/', FollowUser.as_view(),
         name='follow-user'),
    # Список постов на кого подписан
    path('subscriptions/', ListPostSubscriptions.as_view(),
         name='subscriptions'),
]
