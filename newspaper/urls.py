from django.urls import path

from . views import index, category, single, tags

urlpatterns = [
    path('', index, name='index'),
    path('category/<slug:slug>/', category, name='category'),
    path('tags/<slug:slug>/', tags, name='tags'),
    path('single/<slug:slug>/', single, name='single'),
]