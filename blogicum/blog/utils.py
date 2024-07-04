from django.db.models import Count

from blog.models import Post


def count_and_order():
    return Post.published.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
