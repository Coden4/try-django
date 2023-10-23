from django.test import TestCase

from .models import Article
from .utils import slugify_instance_title


class ArticleTestCaes(TestCase):

    def setUp(self):
        self.num_of_articles = 5
        for _ in range(self.num_of_articles):
            Article.objects.create(title='Article', content='Article content')

    def test_queryset_exits(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists)

    def test_queryset_count(self):
        qs = Article.objects.all()
        print(qs.count())
        self.assertEqual(qs.count(), self.num_of_articles)

    def test_article_slug(self):
        article = Article.objects.first()
        self.assertEqual(article.slug, slugify_instance_title(article).slug)

    def test_article_unique_slug(self):
        qs = Article.objects.exclude(slug__iexact='article')
        for article in qs:
            self.assertNotEqual(
                article.slug,
                slugify_instance_title(article).slug
            )

    def test_slugify_instance_title(self):
        article = Article.objects.last()
        slugs = []
        for i in range(self.num_of_articles):
            slugs.append(slugify_instance_title(article, save=False).slug)

        unique_slugs = list(set(slugs))
        self.assertEqual(len(slugs), len(unique_slugs))
