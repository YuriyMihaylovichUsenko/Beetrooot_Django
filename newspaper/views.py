from datetime import datetime
from random import sample

from django.contrib.postgres.search import SearchRank, SearchVector, SearchQuery
from django.db.models import Max, Count, Q
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.contrib import messages

from .models import Article, Comment, Category, Tag, Author
from .forms import CommentForm
from .selectors import (
    related_articles_selector,
    latest_article_selector,
    tags_for_1_article_selector
)
from . utils.send_email import send_email_func


class IndexView(ListView):
    template_name = 'index.html'
    model = Article
    context_object_name = 'articles'
    slug_url_kwarg = 'slug'
    paginate_by = 6
    queryset = Article.objects.prefetch_related(
        'images', 'author'
    ).order_by('-date_news')


class AllArticlesView(ListView):
    template_name = 'category-grid.html'
    model = Article
    context_object_name = 'articles'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        self.category = Category.objects.get(name=self.request.GET['category']) \
            if self.request.GET.get('category') else None
        self.tag = Tag.objects.get(name=self.request.GET['tag']) \
            if self.request.GET.get('tag') else None
        self.author = Author.objects.get(name=self.request.GET['author']) \
            if self.request.GET.get('author') else None
        # self.search = self.request.GET['s'] \
        #     if self.request.GET.get('s') else None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        _filter = {}
        if self.category:
            _filter |= {'category': self.category}
        if self.tag:
            _filter |= {'tags': self.tag}
        if self.author:
            _filter |= {'author': self.author}

        articles = Article.objects.prefetch_related(
            'images', 'category', 'tags', 'author'
        ).filter(**_filter).order_by('-date_news')

        return articles


class SearchView(ListView):
    template_name = 'category-grid.html'
    model = Article
    context_object_name = 'articles'

    def get(self, request, *args, **kwargs):
        self.search = self.request.GET['s'] \
            if self.request.GET.get('s') else None
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        articles = Article.objects.prefetch_related(
            'images', 'category', 'tags', 'author'
        ).annotate(
            rank=self._priority()
        ).filter(
            rank__gte=0.3
        ).order_by(
            '-rank'
        )
        # articles = Article.objects.prefetch_related(
        #     'images', 'category', 'tags', 'author'
        # ).filter(
        #     Q(title_en__icontains=self.search)
        # )
        return articles

    def _priority(self) -> SearchRank:
        if self.request.LANGUAGE_CODE == 'en-us':
            vector = SearchVector('title_en', weight='A') \
                     + SearchVector('description_en', weight='B') \
                     + SearchVector('text_en', weight='A')

            query = SearchQuery(self.search)
            rank = SearchRank(
                vector,
                query,
            )
        else:
            vector = SearchVector('title', weight='A') \
                     + SearchVector('description', weight='B') \
                     + SearchVector('text', weight='A')
            query = SearchQuery(self.search)
            rank = SearchRank(
                vector,
                query,
            )
        return rank


class SingleView(FormView, DetailView):
    template_name = 'single.html'
    model = Article
    context_object_name = 'article'
    slug_url_kwarg = 'slug'
    queryset = Article.objects.prefetch_related('images')
    form_class = CommentForm

    def get_success_url(self):
        return reverse('single', args=(self.get_object().slug,))

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
            'random_articles_2': random_articles_2,
        }

        return context

    def form_valid(self, form):
        data_for_writing = form.cleaned_data | {
            'article': self.get_object(),
            'date_time': datetime.now()
        }
        Comment.objects.create(**data_for_writing)

        messages.add_message(
            self.request, messages.SUCCESS, 'Thank you for comment'
        )

        send_email_func(
            subject='django',
            recipient_list=[form.cleaned_data.get('email')],
            html_template='email.html',
            context={'name': form.cleaned_data.get('name'),
                     'link': self.request.build_absolute_uri(reverse('index'))
                     },
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(
            self.request, messages.WARNING, 'Please input valid data'
        )
        return super().form_invalid(form)


