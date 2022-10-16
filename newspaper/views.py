from random import sample

from django.db.models import Max, Count
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.contrib import messages


from .models import Article, Comment
from .forms import CommentForm
from .selectors import (
    related_articles_selector,
    latest_article_selector,
    tags_for_1_article_selector
)


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'
    slug_url_kwarg = 'slug'
    paginate_by = 6
    queryset = Article.objects.prefetch_related(
        'images', 'author'
    ).order_by('-date_news')


class CategoryView(ListView):
    template_name = 'category-grid.html'
    model = Article
    context_object_name = 'articles'
    slug_url_kwarg = 'slug'
    paginate_by = 2

    def get_queryset(self):
        category_filter = {'category__slug': self.kwargs.get('slug')}
        return Article.objects.prefetch_related(
            'images', 'category'
        ).filter(**category_filter).order_by('-date_news')


class SingleView(FormView, DetailView):
    template_name = 'single.html'
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    queryset = Article.objects.prefetch_related('images')
    form_class = CommentForm

    def get_success_url(self):
        return reverse('single', args=(self.get_object().slug, ))

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
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


    def form_valid(self, form):
        # data_for_writing = form.cleaned_data | {'article': list(self.queryset)[0]}
        data_for_writing = form.cleaned_data | {'article': self.get_object()}
        Comment.objects.create(**data_for_writing)

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

class TagsViews(ListView):
    template_name = 'category-tags.html'
    model = Article
    context_object_name = 'tags'
    slug_url_kwarg = 'slug'
    paginate_by = 2

    def get_queryset(self):
        return Article.objects.prefetch_related(
            'images', 'author'
        ).filter(
            tags__slug=self.kwargs.get('slug')
        ).order_by('-date_news')
