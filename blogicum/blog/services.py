from django.db.models import Count
from django.utils import timezone


def comment_count(posts):
    return posts.select_related(
        'location',
        'author',
        'category',
    ).annotate(
        comment_count=Count('comments')).order_by('-pub_date')


def filtrate_posts(posts):
    return posts.filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    )
