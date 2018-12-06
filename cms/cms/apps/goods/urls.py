from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^goods/recommend/$', views.RecommendGoodsView.as_view()),
    url(r'^goods/category/$', views.GoodsCategoryView.as_view()),
    url(r'^goods/$', views.GoodsListView.as_view()),
    url(r'^category/(?P<pk>\d+)/$', views.Categorys.as_view()),
    url(r'^goods/(?P<goods_id>\d+)/$', views.GoodsDetail.as_view()),
    url(r'^goods/recommand/$', views.GoodsRecommend.as_view())

]
