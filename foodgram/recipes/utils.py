from django.template.defaultfilters import slugify as django_slugify

from unidecode import unidecode


def unique_slugify(value, model):
    index = 0
    base_slug = django_slugify(unidecode(value))
    while True:
        unique_slug = '-'.join([base_slug, str(index)])
        if not model.objects.filter(slug=unique_slug).exists():
            return unique_slug
        index += 1
