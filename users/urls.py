from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.SignUpView.as_view(), name='signup'),
    # path('all_articles/', views.AllArticlesView.as_view(), name='all_articles'),
    ]