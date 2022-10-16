from django.db.models import Count

from .models import Category, Tag, Article


def category_all(request):
    category = Category.objects.all()
    return {'categories': category}


def tags(request):
    tags = Tag.objects.prefetch_related(
        'article'
    ).annotate(
        count_art=Count('article')
    ).order_by('-count_art')[:13]
    return {'tags': tags}


def latest_article(request):
    latest_article = Article.objects.prefetch_related(
            'images').order_by('-date_news')[:3]
    return {'latest_article': latest_article}


