# blog/context_processors.py
"""
The blog app context context processors.
"""
from django.db.models import Count
from . import models

def base_context(request):
    """
    This is the base_context being set so all class in views have access to these
    contexts, and code does not need to be duplicated.
    """
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    latest_posts = models.Post.objects.published() \
        .order_by('-published')[:3]

    topics_list = models.Topic.objects.all().order_by('name')

    top_topics = models.Topic.objects.annotate(post_count=Count('blog_posts')) \
        .order_by('-post_count')[:5]

    posts = models.Post.objects.published().order_by('-published')

    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'topics_list': topics_list,
        'top_topics': top_topics,
        'posts': posts,
    }

    return context
