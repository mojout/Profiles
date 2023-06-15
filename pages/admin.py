from django.contrib import admin
from pages.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    """Некоторые атрибуты: date_hierarchy - навигация по дате по выбранному полю (использует  QuerySet.datetimes());.
    prepopulated_fields - автоматическая генерация значения для полей SlugField из одного или нескольких других полей
    (используется JS); raw_id_fields - используется для удобства, генерирует выпадающий список для выбора и
    осуществляется быстрый переход на страницу выбранного автора, используетсяв связанных полях модели"""

    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'author', 'publish']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
