from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post

User = get_user_model()


# Сокращенный серализатор пользователя
class UserShortSerialiers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class PostSerializers(serializers.ModelSerializer):
    author = UserShortSerialiers()
    is_read_end = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_is_read_end(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.read_end.filter(author=user).exists()
        else:
            return False


# Сокращенный серализатор записи
class PostShortSerializers(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'pub_date']


class UserSerialiers(serializers.ModelSerializer):
    posts = PostShortSerializers(many=True, source='post')
    subscriptions = serializers.SerializerMethodField()
    subscribers = serializers.SerializerMethodField()
    is_subscriber = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'subscriptions',
                  'subscribers', 'is_subscriber', 'posts']

    # Кол-во подписок
    def get_subscriptions(self, obj):
        return obj.subscriber.count()

    # Кол-во подписчиков
    def get_subscribers(self, obj):
        return obj.writer.count()

    # Подписан ли на пользователся
    def get_is_subscriber(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return obj.writer.filter(subscriber=user).exists()
        else:
            return False
