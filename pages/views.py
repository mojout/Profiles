import os
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from .models import Post
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm, SearchForm
from django.db.models import Count
import redis
from django.conf import settings

r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'pages/post/list.html',
                  {'posts': posts,
                   'tag': tag})


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'pages/post/list.html'


def post_detail(request, year, month, day, post):
    """
    Пояснение к агрегированному подсчету тегов через 'Count': 'post_tags_ids' - с помощью атрибута 'flat=True'
    получаем список идентификаторов тегов текущего поста, через запятую([1,2,3]). 'similar_posts' - берем все посты,
    включающие любой из тегов в 'post_tags_ids', за исключением текущего('exclude(id=post.id')). В 'same_tags'
    считаем количество общих тегов, сортируем теги по числу общих тегов и дате публикации. Выводим только последние 4
    поста.
    """

    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = Post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    total_views = r.incr(f'Post:{post.id}:views')

    return render(request, 'pages/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts,
                   'total_views': total_views})


def post_share(request, post_id):
    """
    Идея: Отправка ссылки на пост по e-mail через форму.
    Функционал: Извлекаем пост со статусом 'Published', объявляем переменную 'sent = False' (не
    отправлено), если метод 'POST': создаем экземпляр класса 'EmailPostForm' в переменную form, валидируем
    заполненную форму с помощью 'form.cleaned_data' в переменную 'cd', с помощью метода
    'request.build.get_absolute_uri' с переданным аргументом 'post.get_absolute_url()' сохраняем в переменную
    'post_url' ссылку на пост для вставки в письмо, создаем тему и тело сообщения используя cd и ссылку на пост,
    отправляем письмо и меняем статус переменной 'sent' на 'Отправлено' (True).
    """

    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} поделился с вами постом {post.title}"
            message = f"Читать пост: {post.title} по ссылке {post_url} {cd['name']}'s добавил комментарий: {cd['comments']}"
            send_mail(subject, message, os.getenv('DEFAULT_FROM_EMAIL'), [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'pages/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent})


@require_POST
def post_comment(request, post_id):
    """
    Идея: комментирование постов.
    Функционал: Даем представлению разрешение на метод 'POST'. Извлекаем пост со
    статусом 'Published', объявляем переменную 'comment = None' (не создан), извлекаем форму с ожидаемым методом
    передачи данных 'POST', если форма валидна: сохраняем экземпляр модели без сохранения в БД, назначаем пост
    комментарию, сохраняем комментарий в БД, передаем контекст в шаблон 'comment.html'
    """

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'pages/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})


def post_search(request):
    """Функция поиска будет работать только с БД postgresql, так как были использованы объекты SearchVector
    дистрибутива postgres. Поиск по полям 'title' и 'body'. """

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'), ) \
                .filter(search=query)
    return render(request, 'pages/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
