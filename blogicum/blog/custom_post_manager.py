from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    def related_data(self):
        return self.select_related(
            'location',
            'category',
            'author'
        )

    def published(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )


class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return (
            PostQuerySet(self.model)
            .related_data()
            .published()
        )
