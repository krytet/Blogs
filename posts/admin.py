from django.contrib import admin
from . import models
from .views import spam_massage
import threading


class SaveData(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        print(change)
        if change:
            title = f'У пользователя {obj.author} изменился пост'
            text = f'У пользователя {obj.author} на которого вы подписаны, '+ \
                   f'изменился пост "{obj.title}" можете с ним ' + \
                   f'ознакомся по ссылке <a href="/post/{obj.id}/">кликни</a>'
        else:
            title = f'У пользователя {obj.author} появился новый пост'
            text = f'У пользователя {obj.author} на которого вы подписаны, '+ \
                   f'опубликован новый пост "{obj.title}" можете с ним ' + \
                   f'ознакомся по ссылке <a href="/post/{obj.id}/">кликни</a>'
        th = threading.Thread(target=spam_massage(title, text, obj))
        th.start() 


admin.site.register(models.Post, SaveData)
admin.site.register(models.Subscriptions)
admin.site.register(models.ReadEnd)
