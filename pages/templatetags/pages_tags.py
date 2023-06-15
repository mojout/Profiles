from django import template
from django.db.models import Count

from ..models import Post, Comment

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('pages/post/latest_posts.html')
def show_latest_posts():
    """
    '[:5]' - количество отображаемых статей
    """
    latest_posts = Post.published.order_by('-publish')[:5]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts():
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]