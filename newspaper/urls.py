from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('tags/<slug:slug>/', views.tags, name='tags'),
    path('single/<slug:slug>/', views.SingleView.as_view(), name='single'),
]