from django.contrib import admin
# from django.utils.safestring import mark_safe
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html, mark_safe
from . actions import translate_article, translate_objects
from .models import Image, Article, Tag, Category, Comment, Author


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    fields = ('picture', 'image')
    readonly_fields = fields
    extra = 0


    @staticmethod
    def picture(obj):
        return format_html(
            '<img src="{}" style="max-width: 50px">', obj.image.url
        )


class ArticleAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    actions = [translate_article]
    list_display = ('id', 'title_en', 'translated', 'author', )
    inlines = (ImageInlineAdmin, )
    summernote_fields = ('text', 'text_en')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'text')
    list_filter = ('tags',)
    # list_editable = ('base_url',)

    fieldsets = (
        (None, {
            'fields': (('author'),
                ('base_url', 'slug',),
                ('title', 'title_en'),
                ('text',),
                ('text_en',),
                ('category', ),
                ('tags', ),
                ('date_news', )
            )
        }),
    )

    @staticmethod
    def translated(obj):
        if obj.title_en and obj.text_en and obj.description_en:
            return mark_safe(
                '<img src="/static/admin/img/icon-yes.svg" alt=True>')
        return mark_safe(
            '<img src="/static/admin/img/icon-no.svg" alt="False">')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('picture', )

    def picture(self, obj):
        return format_html(
              '<img src="{}" style="max-width: 50px">', obj.image.url
        )
class TagAdmin(admin.ModelAdmin):
    actions = [translate_objects]
    list_display = ('name', 'name_en', 'count_article', 'id')
    search_fields = ('name', )
    list_editable = ('name_en',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('article')
    @staticmethod
    def count_article(obj):
        count = obj.article.count()
        link = f'/admin/newspaper/article/?tags__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} article</a>')

class AuthorAdmin(admin.ModelAdmin):
    actions = [translate_objects]
    list_display = ('name', 'name_en', 'count_article')
    search_fields = ('name', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('article_set')

    @staticmethod
    def count_article(obj):
        count = obj.article_set.count()
        link = f'/admin/newspaper/article/?author__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} article</a>')

class CategoryAdmin(admin.ModelAdmin):
    actions = [translate_objects]
    list_display = ['name', 'name_en', 'count_articles']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('article_set')

    @staticmethod
    def count_articles(obj):
        count = obj.article_set.count()
        link = f'/admin/newspaper/article/?category__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} article</a>')


admin.site.register(Image, ImageAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Author, AuthorAdmin)
