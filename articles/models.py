from django.db import models
from django.db.models.signals import pre_save, post_save

from .utils import slugify_title


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    slug = models.SlugField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_at = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    # can override
    def save(self) -> None:
        super().save()


def article_pre_save(instance, *args, **kwargs):
    if instance.slug is None:
        slugify_title(instance, save=False)


def article_post_save(instance, created, *args, **kwargs):
    if created:
        slugify_title(instance, save=True)


pre_save.connect(article_pre_save, sender=Article)
post_save.connect(article_post_save, sender=Article)
