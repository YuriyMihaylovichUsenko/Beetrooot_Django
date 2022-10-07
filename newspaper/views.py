from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Category, Article, Tag

def index(request):
    categories = Category.objects.all()
    articles = Article.objects.prefetch_related('images')[:6]
    tags = Tag.objects.prefetch_related(
        'article'
    ).annotate(
        count_art=Count('article')
    ).order_by('-count_art')[:13]
    latest_article = Article.objects.prefetch_related(
        'images').order_by('-date_news')[:3]
    context = {'articles': articles,
               'tags': tags,
                'categories': categories,
               'latest_article': latest_article}
    return render(request, 'index.html', context)


def category(request, **kwargs):
    categories = Category.objects.all()
    categ = get_object_or_404(Category, slug=kwargs.get('slug'))
    art_cat = Article.objects.prefetch_related('images').filter(category=categ)
    tags = Tag.objects.prefetch_related(
        'article'
    ).annotate(
        count_art=Count('article')
    ).order_by('-count_art')[:13]
    latest_article = Article.objects.prefetch_related(
        'images').order_by('-date_news')[:3]
    context = {'articles_some_category': art_cat,
               'tags': tags,
               'category': categ,
                'categories': categories,
               'latest_article': latest_article}
    return render(request, 'category-grid.html', context)


def single(request, **kwargs):
    categories = Category.objects.all()
    article = get_object_or_404(Article, slug=kwargs.get('slug'))
    tags = Tag.objects.prefetch_related(
        'article'
    ).annotate(
        count_art=Count('article')
    ).order_by('-count_art')[:13]
    latest_article = Article.objects.prefetch_related(
        'images').order_by('-date_news')[:3]
    context = {'article': article,
               'tags': tags,
               'categories': categories,
               'latest_article': latest_article}
    return render(request, 'single.html', context)

def tags(request, **kwargs):
    categories = Category.objects.all()
    latest_article = Article.objects.prefetch_related(
        'images').order_by('-date_news')[:3]
    context = {'categories': categories,
               'latest_article': latest_article}
    return render(request, 'category-tags.html', context)
