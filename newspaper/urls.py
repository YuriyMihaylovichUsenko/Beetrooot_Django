from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),
    path('tags/<slug:slug>/', views.TagsViews.as_view(), name='tags'),
    path('single/<slug:slug>/', views.SingleView.as_view(), name='single'),
]