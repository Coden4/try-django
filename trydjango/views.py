"""
   Views get request from django and send response
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from articles.models import Article


def home(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    html = render_to_string('home_view.html', context=context)
    return HttpResponse(html)
