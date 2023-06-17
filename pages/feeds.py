import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post


class LatestPostFeed(Feed):

    """Новостная лента.
    title, link, description - заголовок, ссылка, описание RSS.
    items - возвращает 5 опубликованных статей в новостную ленту.
    item_title, item_description, item_pubdate - возвращает заголовок, описание и дату публикации.
    """

    title = 'IT Digest'
    link = reverse_lazy('pages:post_list')
    description = 'New posts'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.body), 30)

    def item_pubdate(self, item):
        return item.publish


