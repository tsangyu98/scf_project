from django.conf.urls import url

from answers.views import LabelView, QuestionsNewView, QuestionsDoesNotAnswerView, QuestionsHotView, \
    QuestionspublicView, QuestionsDetailView, QuestionsUsefulView, QuestionsUnusefulView, QuestionsReplyView, \
    ReplyusefulView, ReplyUnusefulView, FocusinApiview, LabelUserApiView, FocusoutApiview, LabelDetailsApiView

urlpatterns = [
    url('^labels/$', LabelView.as_view()),
    url('^labels/users/$', LabelUserApiView.as_view()),
    url(r'^questions/-1/label/new/$', QuestionsNewView.as_view()),
    url(r'^questions/-1/label/hot/$', QuestionsHotView.as_view()),
    url(r'^questions/-1/label/wait/$', QuestionsDoesNotAnswerView.as_view()),
    url(r'^questions/$', QuestionspublicView.as_view()),    # 发布问题
    url(r'^questions/(?P<pk>\d+)/$', QuestionsDetailView.as_view()),
    url(r'^questions/(?P<pk>\d+)/useful/$', QuestionsUsefulView.as_view()),
    url(r'^questions/(?P<pk>\d+)/unuseful/$', QuestionsUnusefulView.as_view()),
    url(r'^reply/$', QuestionsReplyView.as_view()),
    url(r'^reply/(?P<pk>\d+)/unuseful/$', ReplyusefulView.as_view()),
    url(r'^reply/(?P<pk>\d+)/useful/$', ReplyUnusefulView.as_view()),
    url(r'^labels/(?P<pk>\d+)/focusin/$', FocusinApiview.as_view()),
    url(r'^labels/(?P<pk>\d+)/focusout/$', FocusoutApiview.as_view()),
    url(r'^labels/(?P<pk>\d+)/$', LabelDetailsApiView.as_view()),
]
