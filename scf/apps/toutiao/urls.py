from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^channels/$', views.HeadlineChannelView.as_view()),
    url(r'^article/(?P<pk>.?\d+)/channel/$', views.ArticleListView.as_view()),
    url(r'^article/(?P<pk>.?\d+)/collect/$', views.CollectOrCancelArticle.as_view()),
    url(r'^article/(?P<pk>.?\d+)/$', views.ArticleDetails.as_view()),
    url(r'^article/$', views.ReleaseArticle.as_view()),
    url(r'^article/(?P<pk>.?\d+)/publish_comment/$', views.CommentArticle.as_view()),
    url(r'^articles/search/$', views.KeywordSearch.as_view()),
]
