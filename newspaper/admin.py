from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from django.utils.html import format_html
from . models import Image, Article, Tag


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
    list_display = ('title', 'base_url', )
    inlines = (ImageInlineAdmin, )
    summernote_fields = ('text', )
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'text')
    list_filter = ('tags',)
    list_editable = ('base_url',)

    fieldsets = (
        (None, {
            'fields': (
                'base_url',
                ('title', 'slug'),
                ('text',),
                ('tags', )
            )
        }),
    )

class ImageAdmin(admin.ModelAdmin):
    list_display = ('picture', )

    def picture(self, obj):
        return format_html(
              '<img src="{}" style="max-width: 50px">', obj.image.url
        )
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'count_article')
    search_fields = ('name', )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('article')
    @staticmethod
    def count_article(obj):
        count = obj.article.count()
        link = f'/admin/newspaper/article/?tags__id__exact={obj.id}'
        return format_html(f'<a href="{link}">{count} article</a>')


admin.site.register(Image, ImageAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag, TagAdmin)
