from django.contrib import admin
from django.urls import path, include

from .views import ListPost, UserProfile, ListPostSubscriptions

urlpatterns = [
    path('', ListPost.as_view(), name='index'),
    path('users/<str:username>/', UserProfile.as_view(), name='user-profile'),
    path('subscriptions/', ListPostSubscriptions.as_view(),
         name='subscriptions'),

]