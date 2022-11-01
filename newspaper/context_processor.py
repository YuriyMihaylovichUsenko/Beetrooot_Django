from datetime import datetime

from django.db.models import Count

from .models import Category, Tag, Article, Author


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


def datetime_now(request):
    return {'datetime_now': datetime.now()}


def authors_most_articles(request):
    mostly_authors = Author.objects.all(
    ).annotate(
        count=Count('article')
    ).order_by('-count')[:13]
    return {'authors_most_articles': mostly_authors}


def most_comments(request):
    most_comments = Article.objects.all(
    ).annotate(
        count_comments=Count('comments')
    ).order_by('-count_comments')
    return {'most_comments': most_comments}


def popular_articles(request):
    popular_articles = Article.objects.all(
    ).order_by('-views')
    print(request)
    return {'popular_articles': popular_articles}
