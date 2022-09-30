from django.urls import path

from . views import index, category, single

urlpatterns = [
    path('', index, name='index'),
    path('category/', category, name='category'),
    path('single/', single, name='single'),
]