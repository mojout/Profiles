from django import forms
from pages.models import Comment


class EmailPostForm(forms.Form):

    """Форма для отправки ссылки на пост по email"""

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):

    """Форма для отправки комментария к посту"""

    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
