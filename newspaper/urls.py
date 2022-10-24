from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('all_articles/', views.AllArticlesView.as_view(), name='all_articles'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('single/<slug:slug>/', views.SingleView.as_view(), name='single'),
]