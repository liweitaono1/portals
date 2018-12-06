from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^news/top/$', views.NewsView.as_view()),
    url(r'^news/category/$', views.NewsCategoryView.as_view()),
]