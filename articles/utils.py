from django.utils.text import slugify
import random


def slugify_instance_title(instance, save=False, new_slug=None):
    slug = new_slug if new_slug is not None else slugify(instance.title)

    klass = instance.__class__
    qs = klass.objects.filter(slug=slug).exclude(id=instance.id)

    if qs.exists():
        # generate unique slugs
        rand_int = random.randint(100_000, 25_500_000)  # Need to verify it
        return slugify_instance_title(instance, save=save, new_slug=f"{slug}-{rand_int}")

    instance.slug = slug
    if save:
        instance.save()

    return instance
