from django.utils.text import slugify
import random


def slugify_title(instance, save=False, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.title)

    qs = instance.__class__.objects.filter(slug=slug).exclude(id=instance.id)

    if qs.exists():
        # generate unique slugs
        rand_int = random.randint(300_000, 500_000)  # Need to verify it
        return slugify_title(instance, save=save, new_slug=f"{slug}-{rand_int}")

    instance.slug = slug
    if save:
        instance.save()

    return instance
