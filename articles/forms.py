from django import forms

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        articles = Article.objects.filter(title__icontains=title)
        if articles.exists():
            self.add_error('title', f'"{title}" already exists.')

        return data

# class ArticleForm(forms.Form):
#     title = forms.CharField()
#     content = forms.CharField()

#     def clean(self):
#         cleaned_data = self.cleaned_data
#         return cleaned_data
