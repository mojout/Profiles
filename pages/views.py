import os

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm


# def post_list(request):
#     post_list = Post.published.all()
#     paginator = Paginator(post_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         posts = paginator.page(page_number)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'pages/post/list.html', {'posts': posts})


def post_share(request, post_id):
    """
    Отправка e-mail через форму. Извлекаем пост со статусом 'Published', объявляем переменную 'sent = False' (не
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


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'pages/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    return render(request, 'pages/post/detail.html', {'post': post})
