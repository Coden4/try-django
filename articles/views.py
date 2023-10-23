from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import Http404

from .models import Article
from .forms import ArticleForm


@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        article = form.save()
        context['article'] = article
        context['created'] = True

    return render(request, 'articles/create.html', context=context)


def article_detail_view(request, slug=None):
    article = None
    if slug is not None:
        try:
            article = Article.objects.get(slug=slug)
        except Article.MultipleObjectsReturned:
            article = Article.objects.filter(slug=slug).first()
        except Article.DoesNotExist:
            raise Http404
        except:
            raise Http404

    context = {
        'article': article
    }

    return render(request, "articles/details.html", context=context)
