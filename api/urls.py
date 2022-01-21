from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, 'users')
router.register('posts', PostViewSet, 'posts')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
