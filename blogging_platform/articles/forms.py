from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'tags']

    content = forms.CharField(required=False)
    tags = forms.CharField(required=False)
