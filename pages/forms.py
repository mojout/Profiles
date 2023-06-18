from django import forms
from pages.models import Comment


class EmailPostForm(forms.Form):

    """Форма для отправки ссылки на пост по email"""

    name = forms.CharField(max_length=25, label='Ваше имя')
    email = forms.EmailField(label='Ваш email')
    to = forms.EmailField(label='email получателя')
    comments = forms.CharField(required=False, label='Комментарий к письму', widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    """Форма для отправки комментария к посту"""

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):

    """Форма поиска"""

    query = forms.CharField(label='Поисковый запрос')
