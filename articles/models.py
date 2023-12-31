from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.db.models import Q
from django.conf import settings

from .utils import slugify_instance_title


class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == '':
            return self.none()

        lookups = Q(title__icontains=query) | Q(content__icontains=query)

        return self.filter(lookups)


class ArticleManager(models.Manager):
    def get_queryset(self) -> ArticleQuerySet:
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None) -> ArticleQuerySet:
        return self.get_queryset().search(query=query)


class Article(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    # custom objects manager
    objects = ArticleManager()

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)


def article_pre_save(instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)


def article_post_save(instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)


pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)
