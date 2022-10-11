from django.db.models import Count, QuerySet

from newspaper.models import Article, Tag


def article_selector():
    return Article.objects.prefetch_related('images')[:6]


def tags_selector():
    return Tag.objects.prefetch_related(
        'article'
    ).annotate(
        count_art=Count('article')
    ).order_by('-count_art')[:13]


def latest_article_selector():
    return Article.objects.prefetch_related(
        'images').order_by('-date_news')[:3]


def tags_for_1_article_selector():
    return Tag.objects.prefetch_related(
        'article'
    ).annotate(
        count_art=Count('article')
    ).order_by('-count_art')[:13]


def related_articles_selector(article: Article) -> QuerySet[Article]:
    return Article.objects.prefetch_related(
        'images'
    ).filter(
        tags__in=article.tags.all()
    ).exclude(
        images__isnull=False, images__image=''
    )

