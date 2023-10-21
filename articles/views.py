from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Article
from .forms import ArticleForm


@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        article = form.save()
        # context['form'] = ArticleForm()  # for clearing all data
        context['article'] = article
        context['created'] = True

    return render(request, 'articles/create.html', context=context)


def article_detail_view(request, id=None):
    article = None
    if id is not None:
        try:
            article = Article.objects.get(id=id)
        except:
            article = None

    context = {
        'article': article
    }

    return render(request, "articles/details.html", context=context)
