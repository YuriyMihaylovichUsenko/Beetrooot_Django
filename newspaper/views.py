from random import sample

from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.generic import TemplateView, DetailView

from . import selectors
from .models import Category, Article, Tag
from .selectors import related_articles_selector, latest_article_selector, \
    tags_for_1_article_selector


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context |= {'articles': selectors.article_selector(),
                    'tags': selectors.tags_selector(),
                    'latest_article': selectors.latest_article_selector()}
        return context


def category(request, **kwargs):
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
               'latest_article': latest_article}
    return render(request, 'category-grid.html', context)


class SingleView(DetailView):
    template_name = 'single.html'
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    queryset = Article.objects.prefetch_related('images')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        random_articles_4 = sample(
            list(related_articles_selector(self.object)), 4)
        random_articles_2 = sample(
            list(related_articles_selector(self.object)), 2)

        context |= {
            'tags': tags_for_1_article_selector,
            'latest_article': latest_article_selector,
            'random_articles_4': random_articles_4,
            'random_articles_2': random_articles_2
        }
        return context


def tags(request, **kwargs):
    latest_article = Article.objects.prefetch_related(
        'images').order_by('-date_news')[:3]
    context = {'latest_article': latest_article}
    return render(request, 'category-tags.html', context)
